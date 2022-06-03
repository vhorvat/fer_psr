#!/usr/bin/env python3
import rosbag
import sys
import math


def getEuclidianDistanceOfTwoDots(x1, y1, x2, y2):
    distance=math.sqrt(math.pow(x2-x1, 2)+math.pow(y2-y1, 2))
    return distance

def getTotalTurtleDistance(xPoses, yPoses):
    overallDistance=0
    for i in range(len(xPoses)-1):
        distance=getEuclidianDistanceOfTwoDots(xPoseArray[i], yPoseArray[i], xPoseArray[i+1], yPoseArray[i+1])
        overallDistance=overallDistance+distance
    return overallDistance

def getTotalActiveTime(tArray):
    time=tArray[len(tArray)-1]-tArray[0]
    return time

def resolutionCorrection(x,y,resolutionX,resolutionY):
    newX=x/resolutionX*800
    newY=y/resolutionY*600
    return newX, newY

def printFollowerData(distance, time, velocity, msg_counter, outbag_filename):
    print(f"Follower turtle")
    print(f"    Covered distance: {round(distance,2)} m")
    print(f"    Average velocity: {round(velocity,2)} m/s")
    print(f"Follower session duration: {round(time,2)} s")
    print(f"Wrote {msg_counter} messages to {outbag_filename}")
    return

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} input.bag')
        sys.exit()

    inbag_filename = sys.argv[1]
    outbag_filename = "processed_follow.bag"

    print(f'Processing input bagfile: {inbag_filename}')

    msg_counter = 0

    xPoseArray=[]
    yPoseArray=[]
    tPoseArray=[]

    with rosbag.Bag(outbag_filename, 'w') as outbag:
        for topic, msg, t in rosbag.Bag(inbag_filename, 'r').read_messages():
            if topic=="/turtle1/pose":
                xPoseArray.append(msg.x)
                yPoseArray.append(msg.y)
                tPoseArray.append(t.to_sec())
                outbag.write("/follower/pose",msg,t)
                msg_counter = msg_counter+1

            if topic=="/mouse_position":
                positionX,positionY=resolutionCorrection(msg.x,msg.y,1680,1050)
                msg.x=round(positionX)
                msg.y=round(positionY)

                outbag.write("/mouse_positions_on_grandparents_computer",msg,t)
                msg_counter = msg_counter+1

        distance=getTotalTurtleDistance(xPoseArray,yPoseArray)
        time=getTotalActiveTime(tPoseArray)
        averageVelocity=distance/time

        printFollowerData(distance, time, averageVelocity, msg_counter, outbag_filename)