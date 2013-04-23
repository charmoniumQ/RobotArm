import glob
from serial.tools import list_ports
import pyfirmata
from config import logs
from config import robot_setup

STEPPER_COMMAND = 0x72
STEPPER_CONFIG = 0
STEPPER_STEP = 1
STEPPER_DRIVER = 1
STEPPER_TWO_WIRE = 2
STEPPER_FOUR_WIRE = 4
STEPPER_ACCEL = 1
STEPPER_DECEL = 2
STEPPER_RUN = 3
STEPPER_CCW = 0
STEPPER_CW = 1
SERVO_MICROS = 0x86


def as_bytes(val, num_bytes=2, size=7):
        return tuple(val / (2 ** (size * x)) % (2 ** size)
                     for x in range(num_bytes))


def regsearch(name):
    return glob.glob(name)


def autodetect():
    return list_ports.comports()


def single_port(name):
    return [name]


class Port(object):  # TODO: test this
    def __init__(self, port_name, log):
        self.log = log
        port = port_name.split(':')
        if logs.core['comm']['__init__']:
            self.log(port)
        if port[0] == 'A':
            self.simulation = False
            self.try_uno_ports(autodetect())
        elif port[0] == 'R':
            self.simulation = False
            self.try_uno_ports(regsearch(port[1]))
        elif port[0] == 'S':
            self.simulation = False
            self.try_uno_ports(single_port(port[1]))
        elif port[0] == 'F':
            self.simulation = True
        else:
            raise ValueError('%s is not a valid option' % port[0])

    def try_uno_ports(self, potential_ports):
        for port in potential_ports:
            try:
                if logs.core['comm']['try_uno_ports']:
                    self.log('Trying: %s' % port)
                self.uno = pyfirmata.Arduino(port,
                    baudrate=robot_setup.baud_rate,
                    name=robot_setup.object_name)
            except Exception as e:
                if logs.core['comm']['try_uno_ports']:
                    self.log('Failed: %s' % port)
                    self.log(str(e))
                pass
            else:
                if logs.core['comm']['successful_port']:
                    self.log('Using port: %s' % port)
                return
        raise RuntimeError('No port found')

    def servo_config(self, pin, min_pulse, max_pulse):
        if logs.core['comm']['servo_config']:
            self.log(('Servo is being setup\n' +
                     'On pin: %d\n' +
                     'With pulse from %d to %d') % (pin, min_pulse, max_pulse))
        if self.simulation:
            return
        self.uno.servo_config(pin, min_pulse, max_pulse)

    def servo_move(self, pin, angle):
        if logs.core['comm']['servo_move']:
            self.log('Servo on pin %d is moving to %d' % (pin, angle))
        if self.simulation:
            return
        self.uno.digital[pin].write(angle)

    def servo_micros(self, pin, micros):
        micros1, micros2 = as_bytes(micros)
        self.uno.send_sysex(SERVO_MICROS, [pin, micros1, micros2])

    def _stepper(self, *data):
        self.uno.send_sysex(STEPPER_COMMAND, list(data))

    def stepper_config_D(self, steps_per_rev, pin1, pin2):
        if logs.core['comm']['stepper_config']:
            self.log(('2 wire stepper being set up\n' +
                     'Steps per revolution: %d\n' +
                     'pins: %d, %d') %
                     (steps_per_rev, pin1, pin2))
        if self.simulation:
            return
        self.steppers += 1
        steps1, steps2 = as_bytes(steps_per_rev)
        self.uno.get_pin(['d', pin1, 'o'])
        self.uno.get_pin(['d', pin2, 'o'])
        self._stepper(STEPPER_CONFIG, self.steppers, STEPPER_DRIVER,
                      steps1, steps2, pin1, pin2)
        return self.setppers

    def stepper_config_2(self, steps_per_rev, pin1, pin2):
        if logs.core['comm']['stepper_config']:
            self.log('2 wire stepper being set up\n' +
                 'Steps per revolution: %d\n' +
                 'pins: %d, %d' %
                 (steps_per_rev, pin1, pin2))
        if self.simulation:
            return
        self.steppers += 1
        steps1, steps2 = as_bytes(steps_per_rev)
        self.uno.get_pin(['d', pin1, 'o'])
        self.uno.get_pin(['d', pin2, 'o'])
        self._stepper(STEPPER_CONFIG, self.steppers, STEPPER_TWO_WIRE,
                      steps1, steps2, pin1, pin2)
        return self.steppers

    def stepper_config_4(self, steps_per_rev, pin1, pin2, pin3, pin4):
        if logs.core['comm']['stepper_config']:
            self.log(('4 wire stepper being setup\n' +
                 'Steps per revolution: %d\n' +
                 'pins: %d, %d, %d, %d') %
                 (steps_per_rev, pin1, pin2, pin3, pin4))
        if self.simulation:
            return
        self.steppers += 1
        steps1, steps2 = as_bytes(steps_per_rev)
        self.uno.get_pin(['d', pin1, 'o'])
        self.uno.get_pin(['d', pin2, 'o'])
        self.uno.get_pin(['d', pin3, 'o'])
        self.uno.get_pin(['d', pin4, 'o'])
        self._stepper(STEPPER_CONFIG, self.steppers, STEPPER_FOUR_WIRE,
                      steps1, steps2, pin1, pin2, pin3, pin4)
        return self.steppers

    def stepper_step(self, stepper_num, direction, steps, speed,
                     accel=None, decel=None):
        if logs.core['comm']['stepper_step']:
            self.log(('Stepper %d is stepping in %d direction for %dsteps' +
                      'at %d speed with an optional accel: %d and decel:%d') %
                 (stepper_num, direction, steps, speed, accel, decel))
        if self.simulation:
            return
        steps1, steps2, steps3 = as_bytes(steps, 3)
        speed1, speed2 = as_bytes(speed)
        if accel is None:
            self._stepper(STEPPER_STEP, stepper_num, direction,
                          steps1, steps2, steps3, speed1, speed2)
        else:
            accel1, accel2 = as_bytes(accel)
            decel1, decel2 = as_bytes(decel),
            self._stepper(STEPPER_STEP, stepper_num, direction,
                          steps1, steps2, steps3, speed1, speed2,
                          accel1, accel2, decel1, decel2)

    def quit(self):
        print 'comm quitting cleanly'
        if self.simulation:
            return
        self.uno.exit()

