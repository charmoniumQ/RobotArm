#import sys
#import os
#sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from framework import joystick, util

joy = joystick.JoystickReader(util.printf)
joy.run()
