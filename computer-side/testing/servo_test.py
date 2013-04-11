#===============================================================================
# OBSOLETE
#===============================================================================

from core import robot
from core import comm

def printy(arg):
    print (arg)

class Struct(object):
    pass


c = comm.Port('F', printy)
f = Struct()
f.log = printy
f.__class__ = robot._Servo
robot._Servo.__init__(f, port=c, pin=1)  # OBSOLETE METHOD SIGNATURE

f.direct_move(0)

print (str(f))

f.direct_move(90)

print (str(f))

f.indirect_move(180)

print (str(f))