from __future__ import print_function
import process
import comm
import time

INCREMENT = 3


class Robot(process.Process):
    def __init__(self, port_name, log_function, servos):
        process.Process.__init__(self, log_function)
        self.log = log_function
        self.port = comm.Port(log_function, port_name)
        self._servos = {}
        for args in servos:
            self._servos[args[0]] = Robot._Servo(self.port, *args[1:])

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

    def __getitem__(self, name):
        return self._servos[name]

    def __str__(self):
        return '\n'.join('%s is at %d' % (name, servo.read())
                         for name, servo in self._servos.items())

    class _Servo:
        def __init__(self, port, pin, min_pulse, max_pulse, start_angle=0,
                     speed=.1):
            self.port = port
            self.pin = pin
            self.speed = speed
            #self.port = None  # TODO: make this an outer class var
            self.port.servo_config(pin, min_pulse, max_pulse)
            self.direct_move(start_angle)

        def direct_move(self, new_angle):  # TODO property for _angle?
            self.port.servo_move(self.pin, new_angle)
            self._angle = new_angle
#            print (self._angle)

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
                    print ('Assert failed')
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

        def read(self):
            return self._angle

        def __str__(self):
            return str(self.read())

#s = Robot('F', print, [('left', 1, 10, 100, 0),
#                       ('right', 2, 10, 100, 0),
#                       ('front', 3, 200, 1000, 50), ])
#s.start()
#s.action_input('print(str(self))')
#s.indirect_move('left', 60)
#s.action_input('print(str(self))')
#time.sleep(2)
#s.indirect_move('right', 60)
#s.action_input('print(str(self))')
#time.sleep(2)
#s.indirect_move('front', 60)
#s.action_input('print(str(self))')
#while not s.idle():
#    pass
#s.quit()
