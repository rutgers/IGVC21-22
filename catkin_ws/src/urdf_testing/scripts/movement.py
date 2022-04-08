#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
PI = 3.1415926535897

def move(speed, distance, isForward):#0,1
    rospy.init_node('robot_cleaner', anonymous=True)
    velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    vel_msg = Twist()

    print("Let's move your robot: ")
  #  speed = float(input("Input your speed: "))
    #distance = input("Input your distance: ")
   # isForward = input("Forward?: ")

    if(isForward):
        vel_msg.linear.x = (speed)
    else:
        vel_msg.linear.x = -(speed)
    vel_msg.linear.y=0
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    vel_msg.angular.z = 0

    t0 = rospy.Time.now().to_sec()
    current_distance = 0

    while not rospy.is_shutdown() and current_distance < distance:
        velocity_publisher.publish(vel_msg)
        t1=rospy.Time.now().to_sec()
        current_distance= (speed)*(t1-t0)
        print(distance - current_distance)
    
    vel_msg.linear.x = 0
    velocity_publisher.publish(vel_msg)

def rotate(speed, angle, clockwise):
    rospy.init_node('robot_cleaner',anonymous=True)
    velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    vel_msg = Twist()

    print("Let's rotate your robot")
    #speed = float(input("Input your speed (degrees/sec):"))
    #angle = float(input("Type your distance (degrees):"))
    #clockwise = float(input("Clockwise?: ")) #true or false

    angular_speed = speed*2*PI/360
    relative_angle = angle*2*PI/360

    vel_msg.linear.x=0
    vel_msg.linear.y=0
    vel_msg.linear.z=0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0

    if clockwise:
        vel_msg.angular.z = -abs(angular_speed)
    else:
        vel_msg.angular.z = abs(angular_speed)

    t0 = rospy.Time.now().to_sec()
    current_angle = 0

    while(current_angle < relative_angle):
        print(current_angle - relative_angle)
        velocity_publisher.publish(vel_msg)
        t1 = rospy.Time.now().to_sec()
        current_angle = angular_speed*(t1-t0)


    vel_msg.angular.z = 0
    velocity_publisher.publish(vel_msg)
    #rospy.spin()


for i in range(5):
    move(4, 4, 1)
    rotate(144, 144, 1)
