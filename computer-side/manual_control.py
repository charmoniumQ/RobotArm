import multiprocessing
import time
import pygame
from pygame import event
from pygame import joystick

simulation = False
UP = 1.5
DOWN = 1/1.5

def runner(robot, joystickid=0):
    queue = multiprocessing.Queue()
    instance = Controller(robot, queue, joystick_id)


class Controller (multiprocessing.Process):
    def __init__(self, robot, queue, joystick_id=0):
        self.bot = robot
        if not simulation:
            if joystick.get_count():
                self.controls = joystick.Joystick(joystick_id)
            else:
                raise BaseException('No joystick detected. Please reconect it')
            self.controls.init()
        else:
            print ('***Using a non-existant joystick***')
        self.mode = self.test
        self.events = queue
        self.quiting = False
        print ('manual control setup!')

    def run(self):
        print ('manual control looping...')
        while not self.quiting:
            self.mode()

    def set_mode(self, new_mode):
        self.mode = new_mode

    def get_axis(self, axis):
        if not simulation:
            return round(self.controls.get_axis(axis) * (5**self.bot.speed / 50), 1)
        else:
            return 0

    def individual(self):
        self.bot.aug('waist', self.get_axis(0))
        if self.controls.get_button(0):
            self.bot.aug('shoulder', self.get_axis(1))
        if self.controls.get_button(3):
            self.bot.aug('elbow', self.get_axis(1))
        if self.controls.get_button(2):
            self.bot.aug('wrist', self.get_axis(1))
        self.bot.aug('claw', self.get_axis(3))
        #if self.get_button == 6:
        #    self.sensitivity(DOWN)
        #if self.get_button == 7:
        #    self.sensitivity(UP)
        if self.get_button == 5:
            self.bot.set('claw', 0)
        if self.get_button == 4:
            self.bot.set('claw', 180)

    def blank(self):
        pass
    
    def sensitivity(self, increment):
        self.bot.robot_speed *= increment

    def test(self):
        time.sleep(.2)
        for ctr in range(5):
            time.sleep(1.5)
            print ('manual_control: %i' % ctr)
        while not self.quiting:
            pass

    def get_axis(self, axis, servo):
        return round(self.controls.get_axis(axis) * self.bot.get_speed(servo) * .005, 1)


    def quit(self):
        self.quiting = True
        del self.controls  # FIXME: do this better
        self.bot.quit()
