import time
import collections
import re
from framework import process, util
from core import comm
from config import robot_setup, logs

R = re.compile(
    ('self\._servos\[{quote}{word}{quote}\]\.{word}\({digit}\)')
    .format(quote='''['"]''', word='(.*?)', digit='([0-0])'))
INCREMENT = 10


class Robot(process.Process):
    def __init__(self, servos, log_function, thread=True):
        process.Process.__init__(self, log_function, thread)
        self.log = log_function
        self.port = comm.Port(robot_setup.port_name, log_function)
        self.sens = 0.07
        self._servos = collections.OrderedDict()
        self.thread = thread
        for args in servos:
            self._servos[args[0]] = _Servo(self, *args[0:])

    def direct_augment(self, servo, angle):
        self.do_action('self._servos[%s].direct_augment(%.3f)' % 
                          (repr(servo), angle))

    def indirect_augment(self, servo, angle):
        self.do_action('self._servos[%s].indirect_augment(.3f)' % 
                          (repr(servo), angle))

    def direct_move(self, servo, angle):
        self.do_action('self._servos[%s].direct_move(%.3f)' % 
                        (repr(servo), angle))

    def indirect_move(self, servo, angle):
        self.do_action('self._servos[%s].indirect_move(%.3f)' % 
                          (repr(servo), angle))

    def sens_r(self, increment):
        print (increment)
        self.do_action('self.sens *= %.6f' % increment)
        if self.sens == 0.0: # lower bound
            self.do_action('self.sens == 0.001')
        print (self.sens)

    def sens_r_up(self):
        self.sens_r(2)

    def sens_r_down(self):
        self.sens_r(.5)

    def sens_s(self, name, increment):
        self.do_action('self._servos["%s"].sens *= %.6f' % (name, increment))
        if self.sens == 0.0:
            self.do_action('self.servos["%s"].sens = .00001' % name)

    def sens_s_up(self, name):
        self.sens_s(2, name)

    def sens_s_down(self, name):
        self.sens_s(.5, name)
    
    # TODO: Properties?
    def get_sensitivity(self, name):
        return self._servos[name].sens * self.sens

    def write_micros(self, servo, micros):
        self.do_action('self._servos[%s].write_micros(%d)' % 
                          (repr(servo), micros))

    def _actually_do_action(self, action):
        # if logs.core['robot']['command']:
            # comm = R.finditer(action)
            # if not int(comm.groups()[2]) == 0:
            #    self.log('%s %s to %s' % comm.groups())
        process.Process._actually_do_action(self, action)
        

    def _quit(self):
        try:
            self.port.close()
            process.Process.quit(self)
        except:
            pass  # already partially destructed

    def __getitem__(self, name):
        return self._servos[name]

    def __str__(self):
        return '\n'.join('%s is at %d' % (name, servo.read())
                         for name, servo in self._servos.items())

class _Servo (object):
    def __init__(self, robot, name, pin, pulse_range=(600, 2400),
                 start_angle=0, valid_range=(0, 180), speed=.1):
        self.robot = robot  # enclosing type
        self.pin = pin
        self.speed = speed
        self.sens = 1.0
        self.name = name
        self.range = valid_range
        self._angle = start_angle
        self.robot.port.servo_config(pin, min(pulse_range), max(pulse_range))
        self.direct_move(start_angle)

    def direct_move(self, extern_angle):  # TODO property for _angle?
        extern_angle = min(180, max(0, extern_angle))
        intern_angle = util.mapi(extern_angle, 0, 180, min(self.range), max(self.range))
        self.robot.port.servo_move(self.pin, intern_angle)
        if not self._angle == extern_angle:
            print ('%s: %.3f' % (self.name, extern_angle))
        self._angle = extern_angle
        if logs.core['robot']['direct_move']:
            self.robot.log('%s servo, Input angle: %d,\nadjusted angle: %d' % 
                           (self.name, extern_angle, intern_angle))
            print (self.pin)

    def indirect_move(self, new_angle):
        try:
            self._angle
        except AttributeError:
            self._angle = 0
        self._time_set()
        while not (self._angle - INCREMENT <= new_angle and
                   new_angle <= self._angle + INCREMENT):
            if new_angle > self._angle + INCREMENT:
                increment = INCREMENT
            elif new_angle < self._angle - INCREMENT:
                increment = -INCREMENT
            else:
                break  # shouldn't ever happen
            self._angle += increment
            self.direct_move(self._angle)
            self._wait()
        self._wait()
        self.direct_move(new_angle)
        self._wait()

    # TODO: properties?
    def _time_get(self):
        return self._time + self.speed < time.time()

    def _time_set(self):
        self._time = time.time()

    def _wait(self):
        while not self._time_get():
            pass
        self._time_set()

    def direct_augment(self, delta_angle):
#        if not delta_angle == 0.0:
#            print '%10s: %f\t\t145' % (self.name, delta_angle)
        self.direct_move(self.read() + delta_angle)

    def indirect_augment(self, delta_angle):
        self.indirect_move(self.angle + delta_angle)

    def write_micros(self, micros):
        self.port.servo_micros(self.pin, micros)

    def read(self):
        return self._angle

    def __str__(self):
        return str(self.read())
