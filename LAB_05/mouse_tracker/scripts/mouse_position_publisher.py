#!/usr/bin/env python3

from pynput.mouse import Controller

import rospy
from geometry_msgs.msg import Point

class MousePositionPublisher:

    def __init__(self):
        self.position_pub = rospy.Publisher("mouse_position", Point, queue_size=1)
        self.position_msg = Point()
        self.mouse = Controller()
        self.rate = rospy.Rate(10)

    def run(self):
        while not rospy.is_shutdown():
            curr_position = self.mouse.position
            self.position_msg.x = curr_position[0]
            self.position_msg.y = curr_position[1]
            self.position_pub.publish(self.position_msg)
            self.rate.sleep()


def main():
  rospy.init_node('mouse_position_publisher', anonymous=True)
  mouse_position_publisher = MousePositionPublisher()
  mouse_position_publisher.run()

if __name__ == '__main__':
    main()
