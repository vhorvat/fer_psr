#!/usr/bin/env python3
import rospy
import math
from geometry_msgs.msg import Point
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
resolution_x = rospy.get_param("/resolution_x") +20  #maloVećiEkranRadiGranica
resolution_y = rospy.get_param("/resolution_y") +20  #maloVećiEkranRadiGranica

class turtle_control():
    
    def point_callback(self, data):
        self.point.x=data.x/resolution_x*11
        self.point.y=(resolution_y-(data.y))/resolution_y*11
        #DEBUGrospy.loginfo(" MIŠ JE NA NORMALIZIRANO: %f  %f" ,self.point.x,self.point.y)

        
    def pose_callback(self, data):
        self.pose.x=data.x
        self.pose.y=data.y
        self.pose.theta=round(data.theta,2)
        #DEBUGrospy.loginfo(" KORNJAČA JE NA NORMALIZIRANO: %f  %f" ,self.pose.x,self.pose.y)

    
    def __init__(self):

        self.turtlePositionSubscriber=rospy.Subscriber("/turtle1/pose", Pose, self.pose_callback) #subscriber na poziciju kornjače
        self.mousePositionSubscriber=rospy.Subscriber("/mouse_position", Point, self.point_callback) #subscriber na poziciju miša
        self.velocityPublisher=rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=1)
        
        self.point=Point()
        self.pose=Pose()
        self.cmd_vel=Twist()

        self.cmd_vel.linear.x=0
        self.cmd_vel.angular.z=0

        self.rate=rospy.Rate(10)
        
    def run(self):
        while not rospy.is_shutdown():
            if abs(self.point.x - self.pose.x)  > 0.2 :
                self.cmd_vel.linear.x=self.get_distance(self.point.x,self.point.y)
                self.cmd_vel.angular.z=self.getang_distance(self.point.x,self.point.y)
            else:
                self.cmd_vel.linear.x=0
                self.cmd_vel.angular.z=0

            self.velocityPublisher.publish(self.cmd_vel)
            self.rate.sleep()


    def get_distance(self, goal_x, goal_y):
        distance = math.sqrt(pow((goal_x-self.pose.x), 2) + math.pow((goal_y-self.pose.y), 2))
        #DEBUGrospy.loginfo(" KORNJAČA JE UDALJENA OD POKAZIVAČA %f" ,distance)
        return distance

    def getang_distance(self , goal_x , goal_y):
        ang_distance = round(math.atan2((goal_y - self.pose.y), (goal_x - self.pose.x)) - self.pose.theta,1)
        return ang_distance*6


if __name__=="__main__":
    try:
        
        rospy.init_node("turtle_control")
        x=turtle_control()
        x.run()
        
    except rospy.ROSInterruptException:
        pass
