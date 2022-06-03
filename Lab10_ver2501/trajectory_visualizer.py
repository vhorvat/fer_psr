#!/usr/bin/env python3
import rospy
from tf2_msgs.msg import TFMessage
from geometry_msgs.msg import Point
from visualization_msgs.msg import Marker

class visualizer():

    def __init__(self):
        self.frame_id=rospy.get_param('~frame_id', 'map')
        self.child_frame_id=rospy.get_param('~child_frame_id', 'pioneer/base_link')
        self.tfTopicSubscriber=rospy.Subscriber("/tf", TFMessage, self.scan)
        self.markerPublisher=rospy.Publisher('robot_positions', Marker, queue_size=1) #LINE_STRIP
        rospy.loginfo("Starting the trajectory visualizer node.")
        rospy.loginfo("frame_id: " + self.frame_id + " child_frame_id: " + self.child_frame_id)
        self.marker=Marker()
        self.marker.header.stamp=rospy.Time(0)
        self.marker.type=Marker.LINE_STRIP
        self.marker.pose.orientation.w=1
        self.marker.color.a=1
        self.marker.color.r, self.marker.color.g, self.marker.color.b = (1., 0, 0)
        self.marker.scale.x = 0.05
        self.marker.scale.y = 0.05
        self.p=Point()

    def scan(self,data):
        if data.transforms:    #filterZaPrazneTransformPoruke
            if data.transforms[0].child_frame_id==self.child_frame_id:
                #rospy.loginfo(data.transforms[0].child_frame_id)
                #rospy.loginfo("n:")
                #rospy.loginfo(self.marker.header.stamp)
                #rospy.loginfo("n+1:")
                #rospy.loginfo(data.transforms[0].header.stamp)
                if self.marker.header.stamp > data.transforms[0].header.stamp:
                    rospy.loginfo("Timestamp has jumped backwards, clearing the trajectory")
                    self.marker.points=[]                                                        
                self.marker.header=data.transforms[0].header
            if data.transforms[0].header.frame_id==self.frame_id and data.transforms[0].child_frame_id==self.child_frame_id:
                p=Point()
                p.x=data.transforms[0].transform.translation.x
                p.y=data.transforms[0].transform.translation.y
                self.marker.points.append(p)
                #rospy.loginfo(p)
            self.markerPublisher.publish(self.marker)
            #rospy.loginfo("Marker published")
        return


    def run(self):
        rospy.spin()

if __name__=="__main__":
    try:
        rospy.init_node('visualizer')
        x=visualizer()
        x.run()

    except rospy.ROSInterruptException:
        pass
