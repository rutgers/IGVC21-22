import odrive
from odrive.enums import *
import time
import hid
import controlParse
import controllerInputs # these two are pretty messy

def init():
    odrv0 = odrive.find_any()
    print(str(odrv0.vbus_voltage))

    if (odrv0.axis0.motor.config.pre_calibrated != True): 
        # calibrate
        print("not calibrated")
        pass 

    print("setting defaults:")

    odrv0.axis0.motor.config.current_lim = 9.4
    odrv0.axis0.motor.config.pole_pairs = 3
    odrv0.axis0.motor.config.torque_constant = 0.05
    odrv0.axis0.encoder.config.cpr = 4096
    # odrv0.axis0.motor.config.current_lim = ?
    odrv0.axis0.controller.config.input_filter_bandwidth = 2.0
    odrv0.axis0.controller.config.vel_gain = 0.045
    odrv0.axis0.controller.config.vel_limit = 40
    odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
    odrv0.axis0.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL

    return odrv0


if __name__ == "__main__":

    odrv0 = init()

    myDeviceName = "Mayflash WiiU Pro Game Controller Adapter"
    myReader = controllerInputs.ControllerReader()
    myReader.openController(myDeviceName)

    while(True):
        output = controlParse.mapControllsTwoStick(myReader.updateInputs())
        odrv0.axis0.controller.input_vel = output['leftMotorTargetSpeed']
        #odrv0.axis1.controller.input_vel = output['rightMotorTargetSpeed']
        print(output)
        time.sleep(0.1)
        

    # note that maximum speed is set to 30 in controlParse.py
    # 40 speed caused motor to draw more than the max set current