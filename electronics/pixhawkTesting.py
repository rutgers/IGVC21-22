#!/usr/bin/env python2.7

from dronekit import connect
import time

vehicle = connect('COM12', wait_ready=True, baud=9600) # port is com12 on my laptop

#print(dir(vehicle)) # shows all functions and properties
#vehicle.play_tune("AAA") # might work with python 2.7, which dronekit is intended for

print("Mode: %s" % vehicle.mode.name)


print(vehicle.gps_0)
print(vehicle.heading) # 0 == north
print(vehicle.system_status)
print(vehicle.velocity)


#Callback to print the location in global frame
def location_callback(self, attr_name, msg):
    print ("Location (Global): ", msg)

#Add observer for the vehicle's current location
vehicle.add_attribute_listener('global_frame', location_callback)

#while True:
#	time.sleep(10) # does this allow the attribute listener to work?