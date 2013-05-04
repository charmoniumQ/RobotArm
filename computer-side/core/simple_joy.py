import time
import pygame
from collections import defaultdict
from framework import joystick, util
from core import robot
from config import robot_setup, logs

class Runner(joystick.JoystickReader):
    def __init__(self, bot=None, log=None, super_quit=util.passf):
        self.super_quit = super_quit
        if log is None:
            flogger = util.FileLogger(robot_setup.log_file)
            log = flogger.log
        if bot is None:
            bot = robot.Robot(robot_setup.servos, log, False)
        self.bot = bot
        joystick.JoystickReader.__init__(self, log, False)
        assert self.controls.get_numaxes() >= 4, "old joystick library, or wrong joystick"
        self.times = defaultdict(lambda:None)
        self.log(self.controls.get_name())

    def joystick(self):
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

    def process_events(self, current):
        if current.type == pygame.JOYBUTTONDOWN:
            if current.button == 6:
                print (self.bot)
                for name, servo in self.bot._servos.iteritems():
                    self.log('sensitivity: %s at N^%.6f * %.6f' % (name, servo.sens_exp, servo.sens))
                self.log('sensitivity: robot at N^%.6f * %.6f' % (self.bot.sens_exp, self.bot.sens))
                return
            elif current.button == 7:
                self.quit()
            # EAST GOAL (NAILS)
            elif current.button == 0:
                self.move_to({'waist':141.163,
                              'shoulder':95.351,
                              'elbow':146.684,
                              'wrist':41,
                              'claw':158.04,})
            # NORTH GOAL (PENCILS)
            elif current.button == 1:
                self.move_to({'waist':94.339,
                              'shoulder':118.826,
                              'elbow':121.568,
                              'wrist':66.48,
                              'claw':158.04,})
            # WEST GOAL (PVC)
            elif current.button == 2:
                self.move_to({'waist':46.13100,
                              'shoulder':95.351,
                              'elbow':146.684,
                              'wrist':41,
                              'claw':158.04,})
            # SPARE
            elif current.button == 3:
                self.move_to({'waist':70.246,
                              'shoulder':24.5,
                              'elbow':154.5,
                              'wrist':41,
                              'claw':0,})
            # LEFT BONUS
            elif current.button == 4:
                self.move_to({'waist':68.5,
                              'shoulder':128.596,
                              'elbow':97.539,
                              'wrist':83.233,
                              'claw':158,})
            # RIGHT BONUS
            elif current.button == 5:
                self.move_to({'waist':122.5,
                              'shoulder':128.94,
                              'elbow':97.539,
                              'wrist':97.55,
                              'claw':158,})
            # HOME (COLLAPSED)
            elif current.button == 8:
                opts = dict((x[0],x[3]) for x in robot_setup.servos)
                self.move_to(opts)
            # READY STATE 
            elif current.button == 9:
                self.move_to({'waist':    96.178,
                              'shoulder': 115.79,})
                time.sleep(0.4)
                self.move_to({'elbow':    162.116,
                              'wrist':    109.143,
                              'claw':     0,})
                time.sleep(0.4)
                self.move_to({'elbow':    162.116,})
            else:
                print current.button

        joystick.JoystickReader.process_events(self, current)

    def adjust_axis(self, name, axis):
        # TODO: scale by time elapsed
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
