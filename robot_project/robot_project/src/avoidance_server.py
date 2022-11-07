#! /usr/bin/python3

# Import the core Python modules for ROS and to implement ROS Actions:
from attr import s
import rospy
import actionlib

# Import all the necessary ROS message types:
from com2009_msgs.msg import SearchFeedback, SearchResult, SearchAction, SearchGoal

# Import the tb3 modules from tb3.py
from tb3_avoidance import Tb3Move, Tb3Odometry, Tb3LaserScan

# Import some other useful Python Modules
from math import sqrt, pow
import numpy as np

class SearchActionServer(object):
    feedback = SearchFeedback() 
    result = SearchResult()

    def __init__(self):
        self.actionserver = actionlib.SimpleActionServer("/search_action_server", 
            SearchAction, self.action_server_launcher, auto_start=False)
        self.actionserver.start()

        self.vel_controller = Tb3Move()
        self.tb3_odom = Tb3Odometry()
        self.tb3_lidar = Tb3LaserScan()
    
    def action_server_launcher(self, goal: SearchGoal):
        r = rospy.Rate(10)
        success = False
        self.tb3_lidar.turn = False
        # Get the current robot odometry:
        self.posx0 = self.tb3_odom.posx
        self.posy0 = self.tb3_odom.posy

        print("The robot will start to move now...")
        # set the robot velocity:
        
        while not success:
            if self.tb3_lidar.min_distance > goal.approach_distance:
                self.vel_controller.set_move_cmd(goal.fwd_velocity, 0.0)
                self.vel_controller.publish()

            elif self.tb3_lidar.min_distance < goal.approach_distance:

                if self.tb3_lidar.turn == True:
                    startTime = rospy.get_rostime()
                    while (rospy.get_rostime().secs - startTime.secs < 2):
                        self.vel_controller.set_move_cmd(0.0, 0.25)
                        self.vel_controller.publish()

                elif self.tb3_lidar.turn == False:
                    startTime = rospy.get_rostime()
                    while (rospy.get_rostime().secs - startTime.secs < 2):
                        self.vel_controller.set_move_cmd(0.0, -0.25)
                        self.vel_controller.publish()

            else:
                success == True
            

            # check if there has been a request to cancel the action mid-way through:
            if self.actionserver.is_preempt_requested():
                rospy.loginfo("Cancelling the camera sweep.")
                self.actionserver.set_preempted()
                # stop the robot:
                self.vel_controller.stop()
                success = False
                # exit the loop:
                break
            
            self.distance = sqrt(pow(self.posx0 - self.tb3_odom.posx, 2) + pow(self.posy0 - self.tb3_odom.posy, 2))
            # populate the feedback message and publish it:
            self.feedback.current_distance_travelled = self.distance
            self.actionserver.publish_feedback(self.feedback)

        if success:
            rospy.loginfo("approach completed sucessfully.")
            self.result.total_distance_travelled = self.distance
            self.result.closest_object_distance = self.tb3_lidar.min_distance
            self.result.closest_object_angle = self.tb3_lidar.closest_object_position

            self.actionserver.set_succeeded(self.result)
            self.vel_controller.stop()
            
if __name__ == '__main__':
    rospy.init_node("search_action_server")
    SearchActionServer()
    rospy.spin()