import time
import pyrealsense2 as rs
import numpy as np
import cv2
import json
from sklearn.linear_model import LinearRegression

class color_command:

    def __init__(self):
        #init camera
        self.pipeline = rs.pipeline()
        config = rs.config()
        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

        # Start streaming
        self.profile = self.pipeline.start(config)

        self.align = rs.align(rs.stream.color)

    def get_color_center(self, lower, upper):

        frames = self.pipeline.wait_for_frames()
        frames = self.align.process(frames)
        depth = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        color_image = np.asanyarray(color_frame.get_data())
        depth_profile = rs.video_stream_profile(self.profile.get_stream(rs.stream.depth))
        intr = depth_profile.get_intrinsics()

        hsv = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)

        lower = np.array(lower)
        upper = np.array(upper)
        contours = None
        if len(lower) & len(upper) == 6:
            mask1 = cv2.inRange(hsv, lower[0:3], upper[0:3])
            mask2 = cv2.inRange(hsv, lower[3:], upper[3:])
            mask = mask1 | mask2
        else:
            mask = cv2.inRange(hsv,lower,upper)
        while contours is None:
            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            #print(contours)
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)
        while M['m00'] == 0:
            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            c = max(contours, key=cv2.contourArea)
            M = cv2.moments(c)

        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        dist_to_center = depth.get_distance(int(cX), int(cY))

        x_cam, y_cam, z_cam = rs.rs2_deproject_pixel_to_point(intr, [cX,cY], dist_to_center)

        center = [x_cam, y_cam, z_cam]


        return center

    def convert_cam_to_arm(self,img):
        
        image_to_arm = np.load("./calibration/save_parms/image_to_arm.npy")
        img = np.array(img)
        img_pos = np.ones(4)
        img_pos[0:3] = img
        #print(img_pos)
        
        arm_pos = np.dot(image_to_arm, img_pos)

        return arm_pos
    
    def form_dict(self,arm_pos):
        keys = np.array(['1','2','3','4','5','6','7','8'])
        color_pairs = zip(keys, arm_pos)
        color_dict = dict(color_pairs)

        return color_dict

    def diff(self,point):
        cali = np.array([137, 108, 85.3, 59.88, 33.6, 9.11, -15.5, -41.6])
        #arm = np.array([114, 86.49, 63.86, 40.75, 16.79, -7.66, -34.3, -58.11])
        arm = np.array([114, 86.49, 63.86, 50.1, 27.79, 4.66, -20.3, -57.11])
        model = LinearRegression()
        model.fit(cali.reshape(-1, 1), arm)

        predicted_value = model.predict(np.array([point]).reshape(-1, 1))
        return predicted_value[0]
