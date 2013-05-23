import time
import process
import pygame
from pygame import joystick, event, display

class JoystickReader(process.Process):
    def __init__(self, log, thread=False):
        '''This is an object reads a joystick with pygame stuff.

        Not actually a new process
        log is the log function
        thread is weather or not to spawn in a new thread (not working yet'''
        # TODO: this is ugly and misleading.
        # It inherits from Process, but it does not actually make another process
        process.Process.__init__(self, log, thread)
        self.pygame_init()
        self.joystick_init()

    def pygame_init(self):
        '''Sets up pygame stuff, called by __init__'''
        pygame.init()
        pygame.register_quit(self.quit)
        joystick.init()
        event.set_allowed(None)
        event.set_allowed([pygame.JOYAXISMOTION, pygame.JOYBALLMOTION,
            pygame.JOYHATMOTION, pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP])
        display.init()
        self.display = display.set_mode([640, 480], flags=pygame.RESIZABLE)

    def joystick_init(self):
        '''Sets up joystick stuff, called by __init__'''
        pygame.init()
        if joystick.get_count() == 0:
            raise RuntimeError('No joystick pluged in')
        if joystick.get_count() > 1:
            raise RuntimeWarning('Too many joysticks plugged in, ' + 
                'defaulting to first')
        self.controls = joystick.Joystick(0)
        self.controls.init()

    def _mode(self):
        '''processes events (calls self.events), and interprets joystick (calls self.joystick)'''
        self.events()
        self.joystick()

    def events(self):
        '''Processes pygame events.

        Don't override this method. If you need to custom process events,
        override self.process_events'''
        event.pump()
        for current in event.get():
            self.process_events(current)

    def process_events(self, current):
        '''processes each event.

        override this method to process events on your own,
        if you promise to call super.process_events'''
        if current.type == pygame.QUIT:
            self.quit()
            return

    def joystick(self):
        '''This interprets the joystick every loop.

        Override this method
        Don't call super, unless you want to'''
        for axis in range(self.controls.get_numaxes()):
            val = self.get_axis(axis)
            time.sleep(.05)
            print '%d: %.3f' % (axis, val)
        print

    def get_axis(self, axis_num):
        '''Gets the position of a joystick as a float between -1.0 and 1.0

        Boilerplate for self.controls.get_axis'''
        self.sanity()
        try:
            val = self.controls.get_axis(axis_num)
        except:
            # TODO: enable logging
            self.quit()
            return 0.0
        return val

    def get_button(self, button_num):
        '''Gets the state of a button as True or False

        Boilerplate for self.controls.get_button'''
        self.sanity()
        try:
            val = self.controls.get_button(button_num)
        except:
            self.quit()
            return False
        return val

    def get_hat(self, hat_num):
        '''Gets the state of a button as a tuple (x_pos, y_pos)
where the pos is either -1, 0 or 1

        Boilerplate for self.controls.get_button'''
        self.sanity()
        try:
            val = self.controls.get_hat(hat_num)
        except:
            self.quit()
            return (0,0)
        return val

    def sanity(self):
        '''Checks to make sure pygame is setup, quits otherwise

        checks to see if joystick module is inited, and if joystick object is setup'''
        try:  # TODO: log this somewhere
            if not joystick.get_init():
                raise RuntimeError('josytick not init')
            if not self.controls.get_init():
                raise RuntimeError('joystick not setup correctly')
        except:
            self.quit()

    def _quit(self):
        try:
            self.controls.quit()
        except pygame.error:
            pass # already destructed
        joystick.quit()
        display.quit()
        pygame.quit()
