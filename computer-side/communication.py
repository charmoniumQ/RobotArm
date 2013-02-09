from serial.tools import list_ports
import serial
import time
import pyfirmata

simulation = False


def get_port(delay, retries=0):
    for x in range(retries + 1):
        for port in list_ports.comports():
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
        if not simulation:
            usb_port = get_port(.1, 10)
            self.uno = pyfirmata.Arduino(usb_port)

#    def _send(self, data):
#        self.uno.send_sysex(pyfirmata.STRING_DATA, data)

    def move(self, pin, angle):
#        if not simulation:
#            self._send([servo, angle])
#        else:
#            print ('%i: %i' % (servo, angle))
        #print ('pin %i to %i degrees' % (pin, angle))
        self.uno.digital[pin].write(angle)

    def servo_config(self, pin, min_pulse=544, max_pulse=2400, angle=0):
        self.uno.servo_config(pin, min_pulse, max_pulse, angle)

    def close(self):
        del self.uno
