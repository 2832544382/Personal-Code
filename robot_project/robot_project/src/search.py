#!/usr/bin/env python3

import rospy
import cv2
from pathlib import Path
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from tb3_search import Tb3Move, Tb3LaserScan
from std_msgs.msg import String
# Import the "argparse" CLI library:
import argparse

class Publisher():
    
    def __init__(self):
        self.node_name = "publisher_cli"
        topic_name = "chatter"

        self.pub = rospy.Publisher(topic_name, String, queue_size=10)
        rospy.init_node(self.node_name, anonymous=True)
        self.rate = rospy.Rate(1) # hz
        
        # Command-Line Interface:
        cli = argparse.ArgumentParser(description=f"Command-line interface for the '{self.node_name}' node.")
        cli.add_argument("-colour", metavar="COL", type=String,
            default="Blue", 
            help="The name of a colour (for example)")

        # obtain the arguments passed to this node from the command-line:
        self.args = cli.parse_args(rospy.myargv()[1:])

        self.ctrl_c = False
        rospy.on_shutdown(self.shutdownhook)

        #task5 init
        self.camera_subscriber = rospy.Subscriber("/camera/rgb/image_raw",
            Image, self.camera_callback)
        self.cvbridge_interface = CvBridge()

        self.robot_controller = Tb3Move()
    
        self.stop_counter = 0

        self.ctrl_c = False

        self.rate = rospy.Rate(5)
        
        self.m00 = 0
        self.m00_min = 10000
        
        

        
        rospy.loginfo(f"The '{self.node_name}' node is active.\n"
                    f"Publishing messages to '/{topic_name}'...")

    def camera_callback(self, img_data):
        try:
            cv_img = self.cvbridge_interface.imgmsg_to_cv2(img_data, desired_encoding="bgr8")
        except CvBridgeError as e:
            print(e)
        
        height, width, _ = cv_img.shape
        crop_width = width - 800
        crop_height = 400
        crop_x = int((width/2) - (crop_width/2))
        crop_y = int((height/2) - (crop_height/2))

        crop_img = cv_img[crop_y:crop_y+crop_height, crop_x:crop_x+crop_width]
        hsv_img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)

        lower_red = (-2,198,100)
        upper_red = (4,255,255)

        lower_blue = (115,225,100)
        upper_blue = (130,255,255)

        lower_green = (59,230,100)
        upper_green = (61,255,255)

        lower_yellow = (27,202,100)
        upper_yellow = (32,255,255)
        
        '''lower_bound = [lower_red,lower_blue,lower_green,lower_yellow]
        upper_bound = [upper_red,upper_blue,upper_green,upper_yellow]
        colors = ["red", "blue", "green", "yellow"]'''

        mask = cv2.inRange(hsv_img, lower_red, upper_red)
        res = cv2.bitwise_and(crop_img, crop_img, mask = mask)
        
        m = cv2.moments(mask)
        self.m00 = m['m00']
        self.cy = m['m10'] / (m['m00'] + 1e-5)

        

        
        base_image_path = Path("robot_project/snap")
        full_image_path = base_image_path.joinpath("pics.jpg")

        cv2.imshow('cropped image', crop_img)
        cv2.waitKey(1)
        if self.m00 > self.m00_min:
            cv2.imwrite(str(full_image_path), crop_img)

    def shutdownhook(self):
        print(f"Stopping the '{self.node_name}' node at: {rospy.get_time()}")
        self.ctrl_c = True

    def main_loop(self):
        while not self.ctrl_c:
            message = f"Searching for something '{self.args.colour.data}' in the environment."
            self.pub.publish(message)

            self.rate.sleep()

if __name__ == '__main__':
    publisher_instance = Publisher()
    try:
        publisher_instance.main_loop()
    except rospy.ROSInterruptException:
        pass