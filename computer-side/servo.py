import multiprocessing
#from math import sqrt, tanh, cosh, degrees
import communication
import Queue
import multiprocessing

comm = communication.Communication()


class Servo (object):
    def __init__(self, pin, min_pulse, max_pulse, start, length, speed):
        comm.servo_config(pin, min_pulse, max_pulse, start)
        self.pin = pin
        self.set(start)
        self.length = length
        self._speed = speed

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
    
    def __str__(self):
        return '%i' % self.read()
    
    def get_speed(self):
        return self._speed
    
    def set_speed(self, speed):
        self._speed = speed
    
    speed = property(get_speed, set_speed)
    angle = property(read, set)


class Stepper (object):
    def __init__(self, interface, steps_per_rev, pin1, pin2, pin3=None, pin4=None):
        self.id = None
        if pin3 is None:
            self.id = comm.stepper_config(interface, steps_per_rev, pin1, pin2)
        else:
            self.id = comm.stepper_config4(interface, steps_per_rev, pin1, pin2, pin3, pin4)

    def step(self, steps, speed):
        direction = 0
        if steps >= 0:
            direction = communication.STEPPER_CW
            steps = +steps
        else:
            direction = communication.STEPPER_CCW
            steps = -steps
        comm.stepper_step(self.id, direction, steps, speed)

class Robot (multiprocessing.Process):
    def __init__(self, servos, speed):
        self._servos = servos
        self.speed = speed
        self.queue = multiprocessing.Queue()
        self.quiting = multiprocessing.Event()
        print ('Robot setup!')
        super(Robot, self).__init__()
        self.start()
    
    def run(self):
        print ('robot looping...')
        while not self.quiting.is_set():
            while not self.queue.empty():
                data = self.queue.pop()
                function = getattr(Servo, data[0])
                servo = self._servos[data[1]]
                angle = data[2]
                function(servo, angle)
                print ('%s: %i' % (servo, angle))
        self._quit()

    #def __getitem__(self, idx):
    #    return self.servos[idx]

    def get_robot_speed(self):
        return self.speed
    
    def set_robot_speed(self, speed):
        self.speed = speed
        
    robot_speed = property(get_robot_speed, set_robot_speed)

    def get_speed(self, servo):
        return self.robot_speed * self._servos[servo].speed
    
    def set_servo_speed(self, servo, speed):
        self._servos[servo].speed = speed
    
    def get_servo_speed(self, servo):
        return self._servos[servo].speed

    def aug(self, servo, angle):
        self.queue.append(('aug', servo, angle))

    def set(self, servo, angle):
        self.queue.append(('set', servo, angle))

    def __str__(self):
        return '\n'.join((name + ': ' +  str(servo)) for (name, servo) in self._servos.items())
        
    def _quit(self): # internal use only
        comm.close()
        self.queue.close()

    def quit(self): # external use
        self.quiting.set()

    #def xyz(x, y, z):
    #    def hypot(leg1, leg2):
    #        return sqrt(leg1**2 + leg2**2)
    #
    #    def cos_law(leg1, leg2, leg3):
    #        '''returns angle opposite leg1'''
    #        return cosh((leg2**2 + leg3**2 - leg1**2)/(2 * leg2 * leg3))
    #
    #    A = self['elbow'].length
    #    C = self['shoulder'].length
    #    L = self['wrist'].lengh
    #    theta = degrees(tanh(y / x))
    #    r = hypot(x, y)
    #    alpha = tanh((z + L) / r)
    #    B = hypot(z + L, r)
    #    a = degrees(cos_law(A, B, C))
    #    b = degrees(cos_law(B, A, C))
    #    c = degrees(cos_law(C, A, B))
    #
    #    print ('wast: %i' % theta)
    #    print ('shoulder: %i' % alpha + a)
    #    print ('elbow: %i' % b)