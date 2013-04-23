import time
import process
import pygame
from pygame import joystick, event

class JoystickReader(process.Process):
    def __init__(self, log, thread=False):
        # TODO: this is ugly and misleading.
        # It inherits from Process, but it doesnot actually make another process
        process.Process.__init__(self, log, thread)
        self.pygame_init()
        self.joystick_init()

    def pygame_init(self):
        pygame.init()
        pygame.joystick.init()
        event.set_allowed(None)
        event.set_allowed([pygame.JOYAXISMOTION, pygame.JOYBALLMOTION,
            pygame.JOYHATMOTION, pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP])

    def joystick_init(self):
        if joystick.get_count() == 0:
            raise RuntimeError('No joystick pluged in')
        if joystick.get_count() > 1:
            raise RuntimeWarning('Too many joysticks plugged in, ' + 
                'defaulting to first')
        self.controls = joystick.Joystick(0)
        self.controls.init()

    def _mode(self):
        self.events()
        self.joystick()

    def events(self):
        event.pump()
        for current in event.get():
            self.process_events(current)

    def process_events(self, current):
        if current.type == pygame.QUIT:
            self.quit()

    def joystick(self):
        for axis in range(self.controls.get_numaxes()):
            val = self.get_axis(axis)
            time.sleep(.05)
            print '%d: %.3f' % (axis, val)
        print

    def get_axis(self, axis_num):
        self.sanity()
        try:
            val = self.controls.get_axis(axis_num)
        except:
            # TODO: enable logging
            self.quit()
            return 0.0
        return val

    def get_button(self, button_num):
        self.sanity()
        try:
            val = self.controls.get_button(button_num)
        except:
            self.quit()
            return False
        return val

    def get_hat(self, hat_num):
        self.sanity()
        try:
            val = self.controls.get_hat(hat_num)
        except:
            self.quit()
            return (0,0)
        return val

    def sanity(self):
        try:  # TODO: log this somewhere
            if not joystick.get_init():
                self.quit()
            if not joystick.get_count():
                self.quit()
            if not self.controls.get_init():
                self.quit()
        except:
            self.quit()

    def _quit(self):
        #TODO: investigate quititng cleanly
        try:
            self.controls.quit()
        except pygame.error:
            pass # already destructed
        joystick.quit()
        pygame.quit()
