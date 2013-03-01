import multiprocessing
import time
import pygame
from pygame import event
from pygame import joystick

JOYSTICK_SIMULATION = False
UP = 1.5
DOWN = 1/1.5


class Controller (multiprocessing.Process):
    def __init__(self, robot, log, joystick_id=0):
        self.bot = robot
        self.log = log
        if not JOYSTICK_SIMULATION:
            if joystick.get_count():
                self.controls = joystick.Joystick(joystick_id)
                self.controls.init()
            else:
                self.log('No joystick detected. Please reconect it')
        else:
            self.log('***Using a non-existant joystick***')
        self.mode = self.test
        self.events = multiprocessing.Queue()
        self.quiting = multiprocessing.Event()
        self.i = 0
        self.delay(0)
        self.log('setup!')
        super(Controller, self).__init__()
        self.start()

    def run(self):
        self.log('looping...')
        self.log('John Chan is cool, but not as cool as Sam Grayson.')
        while not self.quiting.is_set():
            while not self.events.empty():
                function, args = self.events.get()
                function = getattr(self, function)
                function(*args)
            if not self.is_delayed():
                self.mode()
        self._quit()

    def is_delayed(self):
        return self.delay_time > time.time()

    def delay(self, period):
        self.delay_time = time.time() + period
    #
    #def get_axis(self, axis):
    #    if not JOYSTICK_SIMULATION:
    #        return round(self.controls.get_axis(axis) * (5**self.bot.speed / 50), 1)
    #    else:
    #        return 0

    def set_mode_individual(self):
        self.mode = self.individual

    def individual(self):
        try:
            self.bot.aug('waist', self.get_axis(0, 'waist'))
            if self.controls.get_button(0):
                self.bot.aug('shoulder', self.get_axis(1, 'shoulder'))
            if self.controls.get_button(3):
                self.bot.aug('elbow', self.get_axis(1, 'elbow'))
            if self.controls.get_button(2):
                self.bot.aug('wrist', self.get_axis(1, 'wrist'))
            self.bot.aug('claw', self.get_axis(3, 'claw'))
            if self.get_button == 6:
                self.sensitivity(DOWN)
            if self.get_button == 7:
                self.sensitivity(UP)
            if self.get_button == 5:
                self.bot.set('claw', 0)
            if self.get_button == 4:
                self.bot.set('claw', 180)
        except AttributeError:
            pass
            #print ('No Joystick connected')

    def set_mode_keys(self):
        self.mode = self.keys

    def process_keys(self, event):
        pass

    #def keys(self):
    #    while not self.events.empty():
    #        {'F1': lambda self: self.servo = 'waist',
    #         'F2': lambda self: self.servo = 'shoulder',
    #         'F3': lambda self: self.servo = 'elbow',
    #         'F4': lambda self: self.servo = 'wrist',
    #         'F5': lambda self: self.servo = 'claw',}[key.name(event.key)](self)
            
            

    def set_mode_blank(self):
        self.mode = self.blank

    def blank(self):
        pass
    
    def sensitivity(self, increment):
        self.bot.robot_speed *= increment

    def set_mode_test(self):
        self.mode = self.test

    def test(self):
        if self.i == 0:
            self.i = 1
            self.delay(.4)
        elif self.i < 10:
            self.delay(1)
            self.log('%i' % self.i)
            self.i += 1
        else:
            return

    def get_axis(self, axis, servo):
        return round(self.controls.get_axis(axis) * self.bot.get_speed(servo) * .005, 1)


    def quit(self):
        self.quiting.set()

    def _quit(self):
        self.bot.quit()
        self.events.close()