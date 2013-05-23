from config import robot_setup, logs
#TODO: make this more generic; take out robot_setup module, and make it be passed in
from core import comm
from framework import process, util
import collections
import re
import time

R = re.compile(
    ('self\._servos\[{quote}{word}{quote}\]\.{word}\({digit}\)')
    .format(quote='''['"]''', word='(.*?)', digit='([0-0])'))
INCREMENT = 10


class Robot(process.Process):
    def __init__(self, servos, log_function, thread=True):
        '''Makes a robot that manages multiple servos in a thread-safe way.

        servos are a tuple of arguments used to construct servo objects
        log_function is called with messages to log
        thread tells this weather or not to spawn into a new proces.'''
        process.Process.__init__(self, log_function, thread)
        print servos
        self.log = log_function
        self.port = comm.Port(robot_setup.port_name, log_function)
        self.sens = robot_setup.robot_sens
        self.sens_exp = robot_setup.robot_sens_exp
        self._servos = collections.OrderedDict()
        self.thread = thread
        for args in servos:
            print args[0:]
            self._servos[args[0]] = _Servo(self, *args[0:])

    def direct_augment(self, servo, angle):
        '''Asks nicely to move servo by angle, with no delay

        logs:
        logs.core['robot']['movement']
            logs when servo is moving, unless it moves by 0.'''
        self.do_action('self._servos[%s].direct_augment(%.3f)' % 
                          (repr(servo), angle))
        if logs.core['robot']['movement'] and not angle == 0:
            self.log('%s direct_augment by %.3f' % (servo, angle))

    def indirect_augment(self, servo, angle):
        '''Asks nicely to move servo by angle, with a time-dilution, slowing,
based on servo.speed

        logs:
        logs.core['robot']['movement']
            logs when servo is moving, unless it moves by 0.'''
        self.do_action('self._servos[%s].indirect_augment(.3f)' % 
                          (repr(servo), angle))
        if logs.core['robot']['movement'] and not angle == 0:
            self.log('%s indirect_augment by %.3f' % (servo, angle))

    def direct_move(self, servo, angle):
        '''Asks nicely to move servo to angle, with no delay

        logs:
        logs.core['robot']['movement']
            logs when servo is moving, unless it moves by 0.'''
        self.do_action('self._servos[%s].direct_move(%.3f)' % 
                        (repr(servo), angle))
        if logs.core['robot']['movement'] and not angle == self._servos[servo].read():
            self.log('%s direct_move to %.3f' % (servo, angle))

    def indirect_move(self, servo, angle):
        '''Asks nicely to move servo to angle, with a time-dilution, slowing,
based on servo.speed

        logs:
        logs.core['robot']['movement']
            logs when servo is moving, unless it moves by 0.'''
        self.do_action('self._servos[%s].indirect_move(%.3f)' % 
                          (repr(servo), angle))
        if logs.core['robot']['movement'] and not angle == self._servos[servo].read():
            self.log('%s indirect_move to %.3f' % (servo, angle))

    def sens_r(self, increment):
        '''Changes the sensitivity of the robot, by a factor of increment'''
        print (increment)
        if self.sens == 0.0: # lower bound
            self.do_action('self.sens == 0.001')
        self.do_action('self.sens *= %.6f' % increment)
        print (self.sens)

    def sens_r_up(self):
        '''Doubles sensitivity of robot'''
        self.sens_r(2)

    def sens_r_down(self):
        '''Halves sensitivity of robot'''
        self.sens_r(.5)

    def sens_s(self, name, increment):
        '''Changes the sensitivity of the servo named name, by a factor of increment'''
        if self.sens == 0.0:
            self.do_action('self.servos["%s"].sens = .001' % name)
            # If it gets stuck at zero, it isn't movable
            # thats bad.
        self.do_action('self._servos["%s"].sens *= %.6f' % (name, increment))
        # TODO: Is this sensitivity deprecated in favor of Nick's exponent system?

    def sens_s_up(self, name):
        '''Doubles the sensitivity of the servo named name'''
        self.sens_s(2, name)

    def sens_s_down(self, name):
        '''Halves the sensitivity of the servo named name'''
        self.sens_s(.5, name)

    # TODO: Properties?
    def get_sensitivity(self, name):
        '''Gets the total sensitivity of the servo named name,
(after having added in already the sensitivity of the robot'''
        return self._servos[name].sens * self.sens

    def get_sensitivity_exponent(self, name):
        '''Gets the exponenent of sensitivity'''
        return self._servos[name].sens_exp + self.sens_exp

    def write_micros(self, servo, micros):
        '''This is kind of funky'''
        self.do_action('self._servos[%s].write_micros(%d)' % 
                          (repr(servo), micros))

    def _quit(self):
        print ('robot quitting')
        self.port.quit()

    def __getitem__(self, name):
        return self._servos[name]

    def __str__(self):
        return '\n'.join('%8s is at %03.5f => %03.5f' % (name, servo.read(), servo.get_internal_angle())
                         for name, servo in self._servos.items())

class _Servo (object):
    def __init__(self, robot, name, pin, pulse_range=(600, 2400),
                 start_angle=0, valid_range=(0, 180), speed=.1, sens=1.0, sens_exp=1.0,):
        self.robot = robot  # enclosing type
        self.pin = pin
        self.speed = speed
        self.sens = sens
        self.sens_exp = sens_exp
        self.name = name
        self.range = valid_range
        self._angle = start_angle
        self.robot.port.servo_config(pin, min(pulse_range), max(pulse_range))
        self.direct_move(start_angle)

    def direct_move(self, angle):  # TODO property for _angle?
        '''Moves to angle, without speed adjustment'''
        if logs.core['servo']['movement']:
            self.robot.log('servo {:12}, ext ang={:3.2f}'.format(self.name, angle))
        angle = util.clamp(angle, self.range[0], self.range[1])
        if logs.core['servo']['movement']:
            self.robot.log('servo {:12}, clamp  ={:3.2f}'.format(self.name, angle))
        self.robot.port.servo_move(self.pin, angle)
        self._angle = angle

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
