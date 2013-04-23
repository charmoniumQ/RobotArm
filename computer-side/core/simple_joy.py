import time
import pygame
import rpdb2
from collections import defaultdict
from framework import joystick, util
from core import robot
from config import robot_setup, logs

class Runner(joystick.JoystickReader):
    def __init__(self, bot=None, log=util.printf, super_quit=util.passf):
        self.super_quit = super_quit
        if bot is None:
            bot = robot.Robot(robot_setup.servos, util.printf, False)
        self.bot = bot
        joystick.JoystickReader.__init__(self, log, False)
        assert self.controls.get_numaxes() >= 4, "old joystick library, or wrong joystick"
        self.times = defaultdict(time.time)
        self.log(self.controls.get_name())

    def joystick(self):
        self.bot.direct_augment("waist", self.adjust_axis("waist", 2))
        self.bot.direct_augment("shoulder", self.adjust_axis("shoulder", 5))
        self.bot.direct_augment("elbow", self.adjust_axis("elbow", 1))
        self.bot.direct_augment("wrist", self.adjust_axis("wrist", 6))
        self.bot.direct_augment("claw", self.adjust_axis("claw", 7))
        # TODO: claw axis 7
    def get_axis(self, axis):
        if axis > 3:
            return 0.0
        if axis == 7:  # virtual axis
            return self.get_axis(3) - self.get_axis(4)
        else:
            return joystick.JoystickReader.get_axis(self, axis)

    def process_events(self, current):
        if current.type == pygame.JOYBUTTONDOWN:
            if current.button == 0:
                print (self.bot)
                return
            elif current.button == 1:
                for name, servo in self.bot._servos.iteritems():
                    self.log('%s at %.6f' % (name, servo.sens))
                self.log('robot at %.6f' % self.bot.sens)
                return
            elif current.button == 2:
                self.quit()
            elif current.button == 3:
                pass

        joystick.JoystickReader.process_events(self, current)

    def adjust_axis(self, name, axis):
        # TODO: scale by time elapsed
        val = self.get_axis(axis)
        val = self.scale_by_time(name, val)
        val = self.scale_by_sensitivity(name, val)
        if logs.core['simple_joy']['axis_nonzero']:
            if not val == 0.0:
                self.log('%d is at %.3f' % (axis, val))
        return val

    def scale_by_time(self, name, val):
        t = time.time() * 100
        if t - self.times[name] == 0:
            print 0.0
        val = val * (t - self.times[name])
        self.times[name] = t
        return val

    def scale_by_sensitivity(self, name, val):
        val = val * self.bot.get_sensitivity(name)
        return val

    def quit(self):
        print ('simple_joy quitting')
#        rpdb2.settrace()
#        rpdb2.setbreak()
        joystick.JoystickReader.quit(self)
        self.super_quit()

    @staticmethod
    def main():
        f = Runner()
        f.setup()
        while not f.is_quitting():
            f.loop()
        f.end()
if __name__ == '__main__':
    Runner.main()
