from scipy.interpolate import interp1d
import controllerInputs
import time

maxSpeed = 30 # find whatever the max speed of the motor is
deadzone = 30 #maybe add ability for 2 seperate deadzones

mapHigh = interp1d([(255/2)+deadzone,255], [0, maxSpeed])
mapLow = interp1d([0,(255/2)-deadzone], [-1*maxSpeed, 0])

def mapControllsTwoStick(values):
    output = {}

    if(values['firstY'] > (255/2)+deadzone):
        output['leftMotorTargetSpeed'] = round(-1*mapHigh(values['firstY']))
    elif(values['firstY'] < (255/2)-deadzone):
        output['leftMotorTargetSpeed'] = round(-1*mapLow(values['firstY'])) # this could probably be done just by multiplying by -1 but im tired rn
    else:
        output['leftMotorTargetSpeed'] = 0

    if(values['secondY'] > (255/2)+deadzone):
        output['rightMotorTargetSpeed'] = round(-1*mapHigh(values['secondY']))
    elif(values['secondY'] < (255/2)-deadzone):
        output['rightMotorTargetSpeed'] = round(-1*mapLow(values['secondY']))
    else:
        output['rightMotorTargetSpeed'] = 0        

    #print(output)
    return output

def mapControllsTank(values):
    return
    # x axis of controller corresponds to a speed "x", leftSpeed=x, rightSpeed=-x. y axis works exactly the same as twostick. can it only be allowed to move forward and turn one at a time?
    # i didnt think about it but it would probably be able to turn just fine

# this program should be made into a class that can recieve values from controllerInputs.py and get the actual values that we 
# want to write to the motor controller. for now this just means mapping the y axes from the controller input to values between
# -maxSpeed to +maxSpeed

#actually in order to actually make use of the deadzones ill need 2 maps to start mapping where the deadzone ends on + and - side

# also i want 2 control schemes, one thats just one stick per motor and another thats ps1 tank controls

if(__name__ == "__main__"):
#    vals={'firstY': 127}
#    mapControllsTwoStick(vals)

    #myDeviceName = "Controller (XBOX 360 For Windows)"
    myDeviceName = "Mayflash WiiU Pro Game Controller Adapter"
    myReader = controllerInputs.ControllerReader()
    myReader.openController(myDeviceName)

    while(True):
        mapControllsTwoStick(myReader.updateInputs())
        time.sleep(0.25)


# acceleration should be proportional to the difference between target velocity and actual velocity