import time
import process
import pygame
from pygame import joystick, event
from config import logs

class JoystickReader(process.Process):
    def __init__(self, log, thread=False):
        process.Process.__init__(self, log, thread)
        self.pygame_init()
        #self.joystick_init()

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
        print (self.controls.get_name())

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
            print '%d:%d, ' % (axis, (10*val)),
            time.sleep(.05)
        print

    def get_axis(self, axis_num):
        self.sanity()
        val = self.controls.get_axis(axis_num)
        if logs.core['joystick']['axis_nonzero']:
            if not val == 0:
                print '%d: %d' % (axis_num, val)
        return val

    def get_button(self, button_num):
        self.sanity()
        return self.controls.get_button(button_num)

    def get_hat(self, hat_num):
        self.sanity()
        return self.controls.get_hat(hat_num)

    def sanity(self):
        try:
            if not joystick.get_init():
                self.quit()
                self.log('pygame.joystick is not inited')
            if not joystick.get_count():
                self.quit()
                self.log('joystick lost')
            if not self.controls.get_init():
                self.quit()
                self.log('self.controls is not inited')
        except:
            self.log('unknown error')
            self.quit()

    def _quit(self):
        try:
            self.controls.quit()
        except pygame.error:
            pass # already destructed
        joystick.quit()
        pygame.quit()
