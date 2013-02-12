import multiprocessing
import time
import pygame
from pygame import event
from pygame import joystick

JOYSTICK_SIMULATION = True
UP = 1.5
DOWN = 1/1.5


class Controller (multiprocessing.Process):
    def __init__(self, robot, joystick_id=0):
        self.bot = robot
        if not JOYSTICK_SIMULATION:
            if joystick.get_count():
                self.controls = joystick.Joystick(joystick_id)
            else:
                raise BaseException('No joystick detected. Please reconect it')
            self.controls.init()
        else:
            print ('***Using a non-existant joystick***')
        self.mode = self.test
        self.events = multiprocessing.Queue()
        self.quiting = multiprocessing.Event()
        self.i = 0
        super(Controller, self).__init__()

    def run(self):
        print ('manual control looping...')
        while not self.quiting.is_set():
            while not self.events.empty():
                function, args = self.events.get()
                function = getattr(self, function)
                function(*args)
            self.mode()

    def get_axis(self, axis):
        if not JOYSTICK_SIMULATION:
            return round(self.controls.get_axis(axis) * (5**self.bot.speed / 50), 1)
        else:
            return 0

    def set_mode_individual(self):
        self.mode = self.individual

    def individual(self):
        self.bot.aug('waist', self.get_axis(0))
        if self.controls.get_button(0):
            self.bot.aug('shoulder', self.get_axis(1))
        if self.controls.get_button(3):
            self.bot.aug('elbow', self.get_axis(1))
        if self.controls.get_button(2):
            self.bot.aug('wrist', self.get_axis(1))
        self.bot.aug('claw', self.get_axis(3))
        if self.get_button == 6:
            self.sensitivity(DOWN)
        if self.get_button == 7:
            self.sensitivity(UP)
        if self.get_button == 5:
            self.bot.set('claw', 0)
        if self.get_button == 4:
            self.bot.set('claw', 180)

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
            time.sleep(.2)
            self.i = 1
        elif self.i < 5:
            time.sleep(1)
            print ('manual control: %i' % self.i)
            self.i += 1
        else:
            return

    def get_axis(self, axis, servo):
        return round(self.controls.get_axis(axis) * self.bot.get_speed(servo) * .005, 1)


    def quit(self):
        self.quiting.set()
        del self.controls  # FIXME: do this better
        self.bot.quit()
