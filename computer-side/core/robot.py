from framework import process
from core import comm
import time
import re

R = re.compile('self\._servos\[{wildcard}\]\.{wildcard}\({wildcard}\)'
               .format(wildcard='(.*?)'))
INCREMENT = 3


def mapi(val, in_min, in_max, out_min, out_max):
    '''Much like arduino's map.

if val is on a scale between in_min and in_max, 
then the return value is the proportional value on a scale between
out_min and out_max'''
    return int((float(val) - in_min) / (in_max - in_min) *
               (out_max - out_min) + out_min)


class Robot(process.Process):
    def __init__(self, servos, log_function):
        process.Process.__init__(self, log_function)
        self.log = log_function
        self.port = comm.Port(log_function)
        self._servos = {}
        for args in servos:
            self._servos[args[0]] = _Servo(self.port, *args[1:])

    def direct_augment(self, servo, angle):
        self.action_input('self._servos[%s].direct_augment(%d)' %
                          (repr(servo), angle))

    def indirect_augment(self, servo, angle):
        self.action_input('self._servos[%s].indirect_augment(%d)' %
                          (repr(servo), angle))

    def direct_move(self, servo, angle):
        self.action_input('self._servos[%s].direct_move(%d)' %
                          (repr(servo), angle))

    def indirect_move(self, servo, angle):
        self.action_input('self._servos[%s].indirect_move(%d)' %
                          (repr(servo), angle))

    def write_micros(self, servo, micros):
        self.action_input('self._servos[%s].write_micros(%d)' %
                          (repr(servo), micros))

    def _do_action(self, action):
        self.log('hi1')
        if logs.core['robot']['command']:
            comm = R.match(action)
            self.log('hi2')
            self.log('%s %s to %s' % comm.groups())
        process.Process._do_action(self, action)

    #def quit(self):

    def __getitem__(self, name):
        return self._servos[name]

    def __str__(self):
        return '\n'.join('%s is at %d' % (name, servo.read())
                         for name, servo in self._servos.items())


class _Servo:
    def __init__(self, port, pin, pulse_range=(600, 2400), start_angle=0,
                 valid_range=(0, 180), speed=.1):
        self.port = port
        self.pin = pin
        self.speed = speed
        self.range = valid_range
        self.port.servo_config(pin, min(pulse_range), max(pulse_range))
        self.direct_move(start_angle)

    def direct_move(self, new_angle):  # TODO property for _angle?
        mini, maxi = self.range
        adjusted_angle = mapi(new_angle, 0, 180, mini, maxi)
        self.port.servo_move(self.pin, adjusted_angle)
        self._angle = new_angle

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
                increment = - INCREMENT
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
        self.direct_move(self.angle + delta_angle)

    def indirect_augment(self, delta_angle):
        self.indirect_move(self.angle + delta_angle)

    def write_micros(self, micros):
        self.port.servo_micros(self.pin, micros)

    def read(self):
        return self._angle

    def __str__(self):
        return str(self.read())
