#!/usr/bin/env python3
import numpy as np
import rospy
from geometry_msgs.msg import Point
from sensor_msgs.msg import LaserScan
import math
from visualization_msgs.msg import Marker

class carthesian():

    def __init__(self):
        self.scanTopicSubscriber=rospy.Subscriber("scan", LaserScan, self.scan)
        self.markerPublisher=rospy.Publisher('point_positions', Marker, queue_size=1)
        self.marker=Marker()
        self.p=Point()

    def scan(self,data):
        marker=Marker()
        marker.type=Marker.POINTS
        rospy.loginfo(data.header)
        marker.header=data.header
        for i in range(len(data.ranges)):
            p=Point()
            p.x=data.ranges[i]*math.cos(data.angle_min+i*data.angle_increment)
            p.y=data.ranges[i]*math.sin(data.angle_min+i*data.angle_increment)
            marker.points.append(p)
        marker.color.a = 1.
        marker.color.r, marker.color.g, marker.color.b = (1., 0., 0.)
        marker.scale.x = .5
        marker.scale.y = .5
        self.markerPublisher.publish(marker)
        rospy.loginfo("Marker published")
        return


    def run(self):
        while not rospy.is_shutdown():
            a=0

if __name__=="__main__":
    try:
        rospy.init_node('carthesian_points')
        x=carthesian()
        x.run()

    except rospy.ROSInterruptException:
        pass