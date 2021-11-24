import hid
import time

class ControllerReader():

    controller = 0

    def openController(self, myDeviceName):
        for device in hid.enumerate():
            if(device['product_string'] == myDeviceName):
                vid = device['vendor_id']
                pid = device['product_id']
        
                self.controller = hid.Device(vid, pid)

                return print("opened controller")
        print(f"HID device named {myDeviceName} was not found.")

    def closeController(self):
        del self.controller

    def updateInputs(self):
        
        inputs = {}
        report = self.controller.read(64)
        if(report):
            inputs['lb'] = bool(report[10] & 0x10)
            inputs['rb'] = bool(report[10] & 0x20)
            inputs['a'] = bool(report[10] & 0x1)
            inputs['b'] = bool(report[10] & 0x2)
            inputs['x'] = bool(report[10] & 0x8)
            inputs['y'] = bool(report[10] & 0x4)
            inputs['lthree'] = bool(report[11] & 0x1)
            inputs['rthree'] = bool(report[11] & 0x2)
            inputs['up'] = bool(report[11] & 0x4)
            inputs['down'] = bool(report[11] & 0x14)
            inputs['left'] = bool(report[11] & 0x1c)
            inputs['right'] = bool(report[11] & 0xc)
            inputs['zl'] = bool(report[9] & 0xff)  # something about this is wrong not sure what though
            inputs['zr'] = bool(report[9] & 0x0)
            inputs['secondY'] = int(report[7]) #fully up is 0, down is 255
            inputs['secondX'] = int(report[5]) # fully left is 0, right is 255
            inputs['firstY'] = int(report[3])
            inputs['firstX'] = int(report[1])

            return inputs
            # report [6] appears to also be secondY
            # report [4] also appears to be secondX
            # report [8] is 0 if zr&zl are 0 and 0x80 if either is 1
            
def viewAllHid():
    
    devices = []

    for device in hid.enumerate():
        if(device['product_string'] not in devices):
            devices.append(device['product_string'])
    
    print(devices)

if(__name__ == "__main__"):
    viewAllHid()
    
    myDeviceName = "Controller (XBOX 360 For Windows)"
    myReader = ControllerReader()
    myReader.openController(myDeviceName)

    while(True):
        print(myReader.updateInputs())
        time.sleep(0.5)