# C5-E-Controller-API and control handling
 python scripts for setting values in the C5-E motor controller, and interacting with HIDs

not meant to be a comprehensive api, planning on implementing things as needed

controllerInputs.py has a class for reading inputs from a controller, and a function to update all current inputs, pretty generic and will have to be adapted for a radio controller later.
right now it works with xinput controllers and should be easily able to work with dinput controllers with small changes. for using a keyboard it would probably be better to just
use a module made for reading keyboard inputs (keyboard on pypi)

hexEditing.py will maybe be used for changing values for the motor controller, but that might end up not working out, not sure since I dont have acess to the motor controller while writing this

controlParse.py will map the stick values to speeds/torques that can be fed to the motor controller, and any other controls if the need arises.
