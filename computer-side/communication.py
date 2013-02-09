import time
import serial
from serial.tools import list_ports
import pyfirmata

simulation = False


def get_port(delay, retries=0):
    for x in range(retries + 1):
        for port in list(list_ports.comports())[::-1]:
            #list_ports.comports() => [('name', 'description', 'ID')...]
            print ('%s: trying to open' % port[1])
            try:
                comm = serial.Serial(port[0])  # if no exception occurs here,
                                               # then we are successful
                comm.close()
                print ('%s: successfully opened\n' % port[1])
                return port[0]
            except serial.SerialException:
                print ('%s: failed to open\n' % port[1])
            time.sleep(delay)
    raise serial.SerialException('No serial port found')


class Communication (object):
    def __init__(self):
        self.simulation = simulation
        if not self.simulation:
            usb_port = get_port(.2, 5)
            self.uno = pyfirmata.Arduino(usb_port)
        else:
            print ('***Using virtual serial port***')

    def move(self, pin, angle):
        if not self.simulation:
            self.uno.digital[pin].write(angle)
        else:
            pass

    def servo_config(self, pin, min_pulse=544, max_pulse=2400, angle=0):
        print ('servo_config(%i, %i, %i, %i' % (pin, min_pulse, max_pulse, angle))
        if not self.simulation:
            self.uno.servo_config(pin, min_pulse, max_pulse, angle)
        else:
            pass

    def close(self):
        if not self.simulation:
            try:
                del self.uno
            except AttributeError:
                pass # already closed
        else:
            pass