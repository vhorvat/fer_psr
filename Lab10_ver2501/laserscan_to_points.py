#!/usr/bin/env python3
from xml.etree.ElementTree import tostring
import tf2_ros
import rospy
from geometry_msgs.msg import Point
from geometry_msgs.msg import Transform
from geometry_msgs.msg import TransformStamped
from geometry_msgs.msg import Quaternion
from sensor_msgs.msg import LaserScan
import math
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Pose, Point, Quaternion
from nav_msgs.msg import OccupancyGrid
import numpy as np

class carthesian():

    def __init__(self):
        self.current_frame_number=0
        self.frame_id=rospy.get_param('~global_frame', 'map')
        self.accumulate_points=rospy.get_param('~accumulate_points', True)
        self.accumulate_every_n=rospy.get_param('~accumulate_every_n', 50)
        self.tf_buffer=tf2_ros.Buffer()
        self.tf_listner=tf2_ros.TransformListener(self.tf_buffer)
        self.scanTopicSubscriber=rospy.Subscriber("pioneer/scan", LaserScan, self.scan)
        self.markerPublisher=rospy.Publisher('point_positions', Marker, queue_size=1)
        self.marker=Marker()
        self.marker.type=Marker.POINTS
        self.marker.color.a = 1.
        self.marker.color.r, self.marker.color.g, self.marker.color.b = (0.2, 0.8, 1.)
        self.marker.scale.x = .02
        self.marker.scale.y = .02
        self.p=Point()
        self.marker.header.stamp=rospy.Time.now()
        rospy.loginfo("Starting the laser scan visualizer node.")
        rospy.loginfo("Global frame: " + self.frame_id + " accumulate every n: " + str(self.accumulate_every_n))
        #mapTaskDown
        self.pub_map = rospy.Publisher('/map', OccupancyGrid, queue_size=1, latch=True)
        self.grid_msg = OccupancyGrid()
        self.grid_msg.header.stamp = rospy.Time()
        self.grid_msg.header.frame_id = self.frame_id
        self.grid_msg.info.resolution = 0.05
        self.grid_msg.info.width = 1200  # 1200*0.05=60m
        self.grid_msg.info.height = 1200  # 1200*0.05=60m
        self.mapOriginX=0
        self.mapOriginY=0
        self.grid_msg.info.origin = Pose(Point(self.mapOriginX, self.mapOriginY, 0), Quaternion(0, 0, 0, 1)) 
        self.grid = np.ones((self.grid_msg.info.height, self.grid_msg.info.width), dtype=np.int32) *-1
        
        

    def scan(self, data):

        if data.header.stamp < self.marker.header.stamp:
            print('Timestamp has jumped backwards, clearing the buffer.')
            self.marker.header.stamp = data.header.stamp
            self.marker.points.clear()
            self.grid = np.ones((self.grid_msg.info.height, self.grid_msg.info.width),dtype=np.int32) * -1  #mapTask
            self.tf_buffer.clear()
            return

        self.current_frame_number=self.current_frame_number+1
        marker=Marker()
        marker.type=Marker.POINTS
        marker.color.a = 1.
        marker.color.r, marker.color.g, marker.color.b = (0.2, 0.8, 1.)
        marker.scale.x = .04
        marker.scale.y = .04

        marker.header=data.header
        self.marker.header=data.header #hereNededForTimereset
        self.grid_msg.header.stamp = data.header.stamp
   
        #self.tf_buffer.can_transform(self.frame_id, data.header.frame_id, data.header.stamp):
        try:
            transform=self.tf_buffer.lookup_transform(self.frame_id, data.header.frame_id, data.header.stamp)
        except Exception as e:
            #rospy.loginfo(e)
            return

        marker.header.frame_id=self.frame_id
        theta=2*math.atan2(transform.transform.rotation.z, transform.transform.rotation.w)

        
        for i in range(len(data.ranges)):
            p=Point()
            if not data.ranges[i]==0:
                p.x=data.ranges[i]*math.cos(data.angle_min+i*data.angle_increment+theta)+transform.transform.translation.x
                p.y=data.ranges[i]*math.sin(data.angle_min+i*data.angle_increment+theta)+transform.transform.translation.y
            marker.points.append(p)
            self.marker.points.append(p)
            self.grid[int((p.y+self.mapOriginX)/self.grid_msg.info.resolution), int((p.x+self.mapOriginY)/self.grid_msg.info.resolution)] = 100


        if self.accumulate_points and self.current_frame_number==self.accumulate_every_n:
            rospy.loginfo("Makrer published, accumulated")
            self.current_frame_number=0
            self.markerPublisher.publish(self.marker)
            flat_grid = self.grid.reshape((self.grid.size,))
            self.grid_msg.data = list(flat_grid)
            self.pub_map.publish(self.grid_msg)
    
        elif not self.accumulate_points:
            self.markerPublisher.publish(marker)
            rospy.loginfo("Marker published, not accumulated")
        return


    def run(self):
        rospy.spin()

if __name__=="__main__":
    try:
        rospy.init_node('carthesian_points')
        x=carthesian()
        x.run()

    except rospy.ROSInterruptException:
        pass
