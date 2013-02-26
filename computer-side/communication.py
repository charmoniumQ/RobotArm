import time
import serial
from serial.tools import list_ports
import pyfirmata

SERIAL_SIMULATION = True

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


def as_bytes(val, num_bytes, size=7):
        return tuple(val / (2**(7*x)) % (2**7) for x in range(num_bytes))

def get_port(delay, retries=0):
    for x in range(retries + 1):
        for port in list(list_ports.comports())[::-1]:
            #list_ports.comports() => [('name', 'description', 'ID')...]
            #print('%s: trying to open' % port[1])
            try:
                comm = serial.Serial(port[0])  # if no exception occurs here,
                                               # then we are successful
                comm.close()
                #print('%s: successfully opened\n' % port[1])
                return port[0]
            except serial.SerialException:
                pass
                #print('%s: failed to open\n' % port[1])
            time.sleep(delay)
    raise serial.SerialException('No serial port found')


class Communication (object):
    def __init__(self):
        if not SERIAL_SIMULATION:
            usb_port = get_port(.2, 5)
            self.uno = pyfirmata.Arduino(usb_port)
        else:
            pass
            #print('***Using virtual serial port***')
        self.steppers = 0

    def move(self, pin, angle):
        if not SERIAL_SIMULATION:
            self.uno.digital[pin].write(angle)
        else:
            pass
            #print('move: %d to %d' % (pin, angle))

    def servo_config(self, pin, min_pulse=544, max_pulse=2400, angle=0):
        if not SERIAL_SIMULATION:
            self.uno.servo_config(pin, min_pulse, max_pulse, angle)
        else:
            pass
            #print('setup: %d' % pin)

    def stepper(self, *data):
        self.uno.send_sysex(STEPPER_COMMAND, list(data))

    def stepper_config_D(self, steps_per_rev, pin1, pin2):
        self.steppers += 1
        steps1, steps2 = as_bytes(steps_per_rev, 2)
        self.uno.get_pin(['d', pin1, 'o'])
        self.uno.get_pin(['d', pin2, 'o'])
        self.stepper(STEPPER_CONFIG, self.steppers, STEPPER_DRIVER, steps1, steps2, pin1, pin2)
        return self.setppers

    def stepper_config_2(self, steps_per_rev, pin1, pin2):
        self.steppers += 1
        steps1, steps2 = as_bytes(steps_per_rev, 2)
        self.uno.get_pin(['d', pin1, 'o'])
        self.uno.get_pin(['d', pin2, 'o'])
        self.stepper(STEPPER_CONFIG, self.steppers, STEPPER_TWO_WIRE, steps1, steps2, pin1, pin2)
        return self.steppers

    def stepper_config_4(self, steps_per_rev, pin1, pin2, pin3, pin4):
        self.steppers += 1
        steps1, steps2 = as_bytes(steps_per_rev, 2)
        self.uno.get_pin(['d', pin1, 'o'])
        self.uno.get_pin(['d', pin2, 'o'])
        self.uno.get_pin(['d', pin3, 'o'])
        self.uno.get_pin(['d', pin4, 'o'])
        self.stepper(STEPPER_CONFIG, self.steppers, STEPPER_FOUR_WIRE, steps1, steps2, pin1, pin2, pin3, pin4)
        return self.steppers

    def stepper_step(self, stepper_num, direction, steps, speed, accel=None, decel=None):
        steps1, steps2, steps3 = as_bytes(steps, 3)
        speed1, speed2 = as_bytes(speed, 2)
        if accel is None:
            self.stepper(STEPPER_STEP, stepper_num, direction, steps1, steps2, steps3, speed1, speed2)
        else:
            accel1, accel2 = as_bytes(accel, 2)
            decel1, decel2 = as_bytes(decel, 2),
            self.stepper(STEPPER_STEP, stepper_num, direction, steps1, steps2, steps3, speed1, speed2, accel1, accel2, decel1, decel2)

    def close(self):
        if not SERIAL_SIMULATION:
            try:
                del self.uno
            except AttributeError:
                pass # already closed
        else:
            pass