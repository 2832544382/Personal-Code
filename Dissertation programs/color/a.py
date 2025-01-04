import cv2
import numpy as np
import pyrealsense2 as rs
import math
import time
from scipy.optimize import least_squares
from scipy.spatial.transform import Rotation as R

def detect_red_object(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_red = np.array([170, 170, 210])
    upper_red = np.array([175, 200, 255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)
    
    contours, _ = cv2.findContours(mask1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    if len(contours) == 0:
        return None, frame
    
    c = max(contours, key=cv2.contourArea)
    
    M = cv2.moments(c)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
    else:
        return None, frame
    
    return (cX, cY), frame

def move_to_color(centers):
        if centers:
            center = centers  # Assuming we want to move to the first detected center
            image_to_arm = np.load("./save_parms/image_to_arm.npy")
            print(image_to_arm)
            img_pos = np.ones(4)
            img_pos[0:3] = center
            print(center)
            print('##########img_pos')
            print(img_pos)
            arm_pos = np.dot(image_to_arm, np.array(img_pos).T)
            
            print(arm_pos)
            # self.device.move_to(x=arm_pos[0], y=arm_pos[1], z=20, r=0, wait=True)

        # Display the image with centers marked
        cv2.waitKey(1)

def main():
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    
    profile = pipeline.start(config)
    
    try:
        while True:
            frames = pipeline.wait_for_frames()
            depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()
            
            if not depth_frame or not color_frame:
                continue
            
            depth_image = np.asanyarray(depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())
            depth_profile = rs.video_stream_profile(profile.get_stream(rs.stream.depth))
            depth_intrin = depth_profile.get_intrinsics()
            
            center, result_frame = detect_red_object(color_image)            
            if center is not None:
                cX, cY = center
                
                depth = depth_frame.get_distance(cX, cY)
                
                
                #depth_intrin = depth_frame.profile.as_video_stream_profile().intrinsics
                point = rs.rs2_deproject_pixel_to_point(depth_intrin, [cX, cY], depth)
                print('########original')
                print(point)
                time.sleep(2)
                #point_rotated = transform_array(point)
                #print('########rotated')
                #print(point_rotated)
                time.sleep(2)
                
                cv2.putText(result_frame, f"x: {point[0]*1000:.2f}mm y: {point[1]*1000:.2f}mm z: {point[2]*1000:.2f}mm", 
                            (cX - 50, cY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                cv2.circle(result_frame, (cX, cY), 5, (0, 255, 0), -1)
                move_to_color(point)
            
            cv2.imshow('RealSense', result_frame)
            if cv2.waitKey(1) == 27:
                break
    
    finally:
        pipeline.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
