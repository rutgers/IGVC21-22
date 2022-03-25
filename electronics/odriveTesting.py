import odrive
from odrive.enums import *
import time

odrv0 = odrive.find_any()
print(str(odrv0.vbus_voltage))

if (odrv0.axis0.motor.config.pre_calibrated != True): 
	# calibrate
	print("not calibrated")
	pass 




odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
odrv0.axis0.controller.input_pos = 10



