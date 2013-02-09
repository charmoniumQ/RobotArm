import threading
import Queue
import communication
from math import sqrt, tanh, cosh, degrees

comm = communication.Communication()


class Servo (object):
    def __init__(self, pin, min_pulse, max_pulse, start, length):
        self.pin = pin
        comm.servo_config(pin, min_pulse, max_pulse, start)
        self.set(start)
        self.length = length

    def set(self, degrees):
        if 0 <= degrees <= 180:
            comm.move(self.pin, degrees)
            self._angle = degrees
        else:
            #raise ValueError('Servo angle must be between 0 and 180.')
            pass  # fail silently

    def aug(self, offset):
        self.set(self.angle + offset)

    def read(self):
        return self._angle

    angle = property(read, set)


class Robot (threading.Thread):
    def __init__(self, servos, segments=[]):
        self.servos = servos
        self.queue = Queue.Queue()
        self.segments = segments
        threading.Thread.__init__(self)

    def run(self):
        while not self.queue.empty():
            data = self.queue.get()
            function = {'set': Servo.set, 'aug': Servo.aug}[data[0]]
            servo = self.servos[data[1]]
            angle = data[2]
            function(servo, angle)

    def __getitem__(self, idx):
        return self.servos[idx]

    def aug(self, servo, angle):
        self.queue.put(('aug', servo, angle))

    def set(self, servo, angle):
        self.queue.put(('set', servo, angle))

    def xyz(x, y, z):
        def hypot(leg1, leg2):
            return sqrt(leg1**2 + leg2**2)

        def cos_law(leg1, leg2, leg3):
            '''returns angle opposite leg1'''
            return cosh((leg2**2 + leg3**2 - leg1**2)/(2 * leg2 * leg3))

        A = self['elbow'].length
        C = self['shoulder'].length
        L = self['wrist'].lengh
        theta = degrees(tanh(y / x))
        r = hypot(x, y)
        alpha = tanh((z + L) / r)
        B = hypot(z + L, r)
        a = degrees(cos_law(A, B, C))
        b = degrees(cos_law(B, A, C))
        c = degrees(cos_law(C, A, B))

        print ('wast: %i' % theta)
        print ('shoulder: %i' % alpha + a)
        print ('elbow: %i' % b)
