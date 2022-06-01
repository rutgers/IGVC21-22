#!/usr/bin/env python

import time
import serial
import glob
#import keyboard
import platform
import sys
import rospy
from std_msgs.msg import String

if(platform.system() != "Linux"):
	sys.exit("Linux only")

while(True):
	probable_port = glob.glob("/dev/ttyUSB*")
	if len(probable_port) > 0:
		ser = serial.Serial(probable_port[0], 9600, timeout = 5)
		print("Connected")
		break
	time.sleep(1)
	print("Looking for Arduino")


def callback(data):
	if data == "autonomous":
		ser.write('a'.encode('utf-8')) # just a character for the arduino to recieve 
	else:
		ser.write('b'.encode('utf-8'))


def listener():

	rospy.init_node('listener', anonymous=True)
	rospy.Subscriber("vehicle_state", String, callback)
	rospy.spin()

# testing

# while(True):
# 	key = keyboard.read_key()
# 	print("key pressed:", end="")
# 	print(key)

# 	ser.write(key.encode('utf-8'))


