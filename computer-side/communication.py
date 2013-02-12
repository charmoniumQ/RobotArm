import time
import serial
from serial.tools import list_ports
import pyfirmata

SERIAL_SIMULATION = True
CONSOLE_OUTPUT = False
def print_function(*args):
    if CONSOLE_OUTPUT:
        print args


def get_port(delay, retries=0):
    for x in range(retries + 1):
        for port in list(list_ports.comports())[::-1]:
            #list_ports.comports() => [('name', 'description', 'ID')...]
            print_function('%s: trying to open' % port[1])
            try:
                comm = serial.Serial(port[0])  # if no exception occurs here,
                                               # then we are successful
                comm.close()
                if CONSOLE_OUTPUT:
                    print_function('%s: successfully opened\n' % port[1])
                return port[0]
            except serial.SerialException:
                print_function('%s: failed to open\n' % port[1])
            time.sleep(delay)
    raise serial.SerialException('No serial port found')


class Communication (object):
    def __init__(self):
        if not SERIAL_SIMULATION:
            usb_port = get_port(.2, 5)
            self.uno = pyfirmata.Arduino(usb_port)
        else:
            print ('***Using virtual serial port***')

    def move(self, pin, angle):
        if not SERIAL_SIMULATION:
            self.uno.digital[pin].write(angle)
        else:
            print_function('move: %d to %d' % (pin, angle))

    def servo_config(self, pin, min_pulse=544, max_pulse=2400, angle=0):
        if not SERIAL_SIMULATION:
            self.uno.servo_config(pin, min_pulse, max_pulse, angle)
        else:
            print_function('setup: %d' % pin)

    def close(self):
        if not SERIAL_SIMULATION:
            try:
                del self.uno
            except AttributeError:
                pass # already closed
        else:
            pass