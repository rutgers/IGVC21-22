## odrive stuff and control handling

odriveTesting.py shows the config and commands to get the motor running.

controllerInputs.py has a class for reading inputs from a controller, and a function to update all current inputs, pretty generic, not important but I wanted to make it

controlParse.py will map the stick values to speeds/torques that can be fed to the motor controller, and any other controls if the need arises.
