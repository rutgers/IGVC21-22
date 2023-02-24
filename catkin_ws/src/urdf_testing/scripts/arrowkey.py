import pygame
from geometry_msgs.msg import Twist
import rospy

pygame.init()
BLACK = (0,0,0)
WIDTH = 1280
HEIGHT = 1024
windowSurface = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
windowSurface.fill(BLACK)

pub = rospy.Publisher('/z_differential/cmd_vel', Twist, queue_size=10)
rospy.init_node('talker', anonymous=True)
rate = rospy.Rate(10) # 10hz
while not rospy.is_shutdown():
    
    t = Twist()
    t.linear.x = 0
    t.angular.z = 0
    keys = pygame.key.get_pressed()  #checking pressed keys
    if keys[pygame.K_UP]:
        t.linear.x += 1
    if keys[pygame.K_DOWN]:
        t.linear.x -= 1
    if keys[pygame.K_LEFT]:
        t.angular.z +=1
    if keys[pygame.K_RIGHT]:
        t.angular.z -=1

    pub.publish(t)
    rate.sleep()
    pygame.event.pump()