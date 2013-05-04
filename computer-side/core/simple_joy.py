import sys
import time
import functools
import pygame
from pygame import key, display
from collections import defaultdict
from framework import joystick, util, process
from core import robot
from config import robot_setup, logs, commands

f = functools.partial
simulation = True

class Runner(joystick.JoystickReader, process.Process):
    def __init__(self, bot=None, log=None, super_quit=util.passf):
        self.super_quit = super_quit
        if log is None:
            #flogger = util.FileLogger(logs.log_file)
            #log = flogger.log
            log = util.printf
        if bot is None:
            bot = robot.Robot(robot_setup.servos, log, False)
        self.bot = bot
        if not simulation:
            joystick.JoystickReader.__init__(self, log, False)
            assert self.controls.get_numaxes() >= 4, (
            "old joystick library, or wrong joystick")
            self.log(self.controls.get_name())
        else:
            # replacement for the above
            process.Process.__init__(self, log, False)
            pygame.init()
            display.init()
            self.display = display.set_mode([640, 480], pygame.RESIZABLE)
        self.times = defaultdict(lambda:None)

    def joystick(self):
        if not simulation:
            self.bot.direct_augment("waist", self.adjust_axis("waist", 2))
            self.bot.direct_augment("shoulder", self.adjust_axis("shoulder", 5))
            self.bot.direct_augment("elbow", self.adjust_axis("elbow", 1))
            self.bot.direct_augment("wrist", self.adjust_axis("wrist", 6))
            self.bot.direct_augment("claw", self.adjust_axis("claw", 7))

    def move_to(self, args):
        for k,v in args.iteritems():
            #TODO: indirect_move?
            self.bot.direct_move(k, v)

    def get_axis(self, axis):
        if axis == 7:  # virtual axis
            return (self.get_axis(3) - self.get_axis(4))/2.0
        else:
            return joystick.JoystickReader.get_axis(self, axis)

    def joybuttondown(self, button):
        try:
            commands.joystick_buttons[button]()
        except KeyError:
            if logs.core['simple_joy']['unmapped_key']:
                self.log(button)
        except:
            if logs.core['simple_joy']['error']:
                self.log(button + ' ' + sys.exc_info)

    def do_key(self, key):
        try:
            func = commands.keyboard[key]
        except KeyError:  # print out unknown key
            if logs.core['simple_joy']['unmapped_key']:
                func = lambda self: self.log('Unmapped key: %s' % key)
            else:
                func = lambda _: util.passf
        else:
            if logs.core['simple_joy']['do_key']:
                print ('Key: {k}, doing {f!s}'
                       .format(k=key, f=func))
        func(self)

    def process_events(self, current):
        if current.type == pygame.JOYBUTTONDOWN:
            self.joybuttondown(current.button)
        elif current.type == pygame.KEYUP:
            self.do_key(key.name(current.key))

        joystick.JoystickReader.process_events(self, current)

    def _mode(self):
        if not simulation:
            joystick.JoystickReader._mode(self)
        else:
            #replacement for the above
            self.events()

    def adjust_axis(self, name, axis):
        val = self.get_axis(axis)
        #print 'aa {:6} ax={:2} val init = {:03.9f}'.format(name, axis, val)
        val = self.scale_by_sensitivity(name, val)
        #print 'aa {:6} ax={:2} val sbs  = {:03.9f}'.format(name, axis, val)
        val = self.scale_by_time(name, val)
        #print 'aa {:6} ax={:2} val sbt  = {:03.9f}'.format(name, axis, val)
        if logs.core['simple_joy']['axis_nonzero']:
            if not round(val, 2) == 0.0:
                self.log('adjusting %d to %.3f' % (axis, val))
        return val

    def scale_by_time(self, name, val):
        t = time.time() * 100
        if self.times[name] is None:
            self.times[name] = t
            return 0
        if t - self.times[name] == 0:
            return 0
        dt = t - self.times[name]
        dt = util.clamp(dt, 0, 25) # Clamp elapsed time to 0.25 second to prevent jerking
        val = val * dt
        self.times[name] = t
        return val

    def scale_by_sensitivity(self, name, val):
        #print 'sensitivity:', name, val
        # OLD METHOD
        #val = val * self.bot.get_sensitivity(name)

        sens = self.bot.get_sensitivity(name)

        exp = self.bot. get_sensitivity_exponent(name)
        sign = -1 if val < 0 else 1 
        val = sign * (abs(float(val))**exp)
        val *= sens

        # Limit motion to some maximum speed (per 1/00th of a second)
        ##val = sign * min(abs(val), 0.1)

        return val

    def quit(self):
        print ('simple_joy quitting')
        if not simulation:
            joystick.JoystickReader.quit(self)
        else:
            display.quit()
            pygame.quit()
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
