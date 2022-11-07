#!/usr/bin/env python3

from re import T
import rospy
import time
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from math import sqrt, pow, pi, degrees



class task1:
    def callback_function(self, odom_data):
        or_x = odom_data.pose.pose.orientation.x
        or_y = odom_data.pose.pose.orientation.y
        or_z = odom_data.pose.pose.orientation.z
        or_w = odom_data.pose.pose.orientation.w
        position_x = odom_data.pose.pose.position.x
        position_y = odom_data.pose.pose.position.y

        (roll, pitch, yaw) = euler_from_quaternion([or_x, or_y, or_z, or_w], 'sxyz')
        
        self.x = position_x
        self.y = position_y
        self.theta_z = yaw

        if self.startup:
            self.startup = False
            self.x0 = self.x
            self.y0 = self.y
            self.theta_z0 = self.theta_z

        print(f"x={round(self.x, 2)} [m], y={round(self.y, 2)} [m], yaw={round(degrees(self.theta_z), 1)} [degrees]")
        

    def __init__(self):
        pub_topic = "/cmd_vel"
        sub_topic = "odom"
        node_name = "task1"

        self.pub = rospy.Publisher(pub_topic, Twist, queue_size=10)
        self.sub = rospy.Subscriber(sub_topic, Odometry, self.callback_function)

        self.ctrl_c = False
        rospy.on_shutdown(self.shutdownhook)

        self.startup = True
        self.secondLoop = False

        self.x = 0.0
        self.y = 0.0
        self.theta_z = 0.0
        self.x0 = 0.0
        self.y0 = 0.0
        self.theta_z0 = 0.0

        rospy.init_node(node_name, anonymous=True)
        self.rate = rospy.Rate(1)
        
        self.vel = Twist()
    
    def shutdownhook(self):
        self.pub.publish(Twist())
        self.ctrl_c = True

    
    def main_loop(self):
        Initial = time.time()
        while not self.ctrl_c:
            if self.startup:
                self.vel = Twist()
            elif self.secondLoop:
                if abs(round(self.x,4) - round(self.x0,4)) <= 0.0005 and time.time() - Initial > 50:
                    self.vel = Twist()
                    self.ctrl_c = True
                    
                else:
                    self.vel = Twist()
                    radius = -0.5
                    lin_vel = 0.105

                    self.vel.linear.x = lin_vel
                    self.vel.angular.z = lin_vel /radius
                    
            else:
                if abs(round(self.x,4) - round(self.x0,4)) <= 0.0005 and time.time() - Initial > 25 :
                    self.secondLoop = True
                    self.vel = Twist()

                else:
                    self.vel = Twist()
                    radius = 0.5
                    lin_vel = 0.105
                    
                    self.vel.linear.x = lin_vel
                    self.vel.angular.z = lin_vel /radius
                    

            self.pub.publish(self.vel)
            #self.rate.sleep()

if __name__ == '__main__':
    task1_instance = task1()
    try:
        task1_instance.main_loop()
    except rospy.ROSInterruptException:
        pass