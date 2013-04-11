import pygame
from framework import joystick, util
from core import robot
from config import robot_setup, logs

#import os
#os.system('echo | env | grep LD_LIBRARY_PATH')
#import sys
#sys.exit()

class Runner(joystick.JoystickReader):
    def __init__(self):
        self.bot = robot.Robot(robot_setup.servos, util.printf, False)
        joystick.JoystickReader.__init__(self, util.printf, False)
        self.bot.sens_s('shoulder', .7)
        assert self.controls.get_numaxes() >= 4, "OLD JOYSTICK LIBRARY"

    def joystick(self):
        self.bot.direct_augment("waist", self.adjust_axis("waist", 2))
#        self.bot.direct_move("shoulder", 56)
        self.bot.direct_augment("shoulder", self.adjust_axis("shoulder", 5))
        self.bot.direct_augment("elbow", self.adjust_axis("elbow", 1))
        self.bot.direct_augment("wrist", self.adjust_axis("wrist", 6))
        self.bot.direct_augment("claw", self.adjust_axis("claw", 7))
        # TODO: claw axis 7
    def get_axis(self, axis):
        if axis in (2, 5):
            if self.get_button(11):
                return 0
        if axis in (0, 1):
            if self.get_button(10):
                return 0
        if axis == 7:
            return self.get_axis(3) - self.get_axis(4)
        else:
            return joystick.JoystickReader.get_axis(self, axis)

    def process_events(self, current):
        if current.type == pygame.QUIT:
            self.quit()
        if current.type == pygame.JOYBUTTONDOWN:
            # TODO: boilerplate
            inc = 0.0
            if current.button == 4:
                inc = 0.8
            elif current.button == 5:
                inc = 1.25
            elif current.button == 0:
                print (self.bot)
                return
            elif current.button == 1:
                for name, servo in self.bot._servos.iteritems():
                    print ('%s at %.6f' % (name, servo.sens))
                print ('robot at %.6f' % self.bot.sens)
                return
            elif current.button == 2:
                self.quit()
            else:
                return
                #TODO: modular
            hat = self.get_hat(0)
            if hat == (0, 1):
                self.bot.sens_s('waist', inc)
            if hat == (1, 0):
                self.bot.sens_s('shoulder', inc)
            if hat == (0, -1):
                self.bot.sens_s('elbow', inc)
            if hat == (-1, 0):
                self.bot.sens_s('wrist', inc)
            if hat == (0, 0):
                self.bot.sens_r(inc)
        
        joystick.JoystickReader.process_events(self, current)

    def adjust_axis(self, name, axis):
        # TODO: scale by time elapsed
        val = self.get_axis(axis)
        if logs.testing['simple_joy']['axis_nonzero']:
            if not val == 0.0:
                print '%d is at %d' % (axis, val)
        return self.bot.get_sensitivity(name) * val

    @staticmethod
    def main():
        Runner().run()

    def _mode(self):
#        for name, servo in self.bot._servos.items():
#            print '%s: %d' % (name, servo.read()),
#        print
        joystick.JoystickReader._mode(self)

Runner.main()
