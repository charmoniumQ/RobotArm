import time
import pygame
import sys
import multiprocessing
from pygame import display
from pygame import event
from pygame import key
import reader
import servo
import manual_control
import automatic_control


class App(object):
    def __init__(self):
        ### pygame setup ###
        pygame.init()
        self.screen = display.set_mode((800, 600))
        display.set_caption('Control a Robotic Arm!')
        event.set_blocked([pygame. ACTIVEEVENT, pygame.KEYUP,
            pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN,
            pygame.JOYBALLMOTION, pygame.JOYHATMOTION, pygame.JOYBUTTONUP,
            pygame.VIDEORESIZE, pygame.VIDEOEXPOSE, pygame.USEREVENT,
            pygame.JOYAXISMOTION])
        pygame.register_quit(self.quit)
        self.text = {'master': reader.Reader("master process", (10,10), 380, 12, height=280, bg=(0,30,30), fgcolor=(255,255,255)),
                     'bot': reader.Reader("bot process", (400,10), 380, 12, height=280, bg=(0,30,30), fgcolor=(255,255,255)),
                     'automatic_control': reader.Reader("automatic_control process", (10,300), 380, 12, height=280, bg=(0,30,30), fgcolor=(255,255,255)),
                     'manual_control': reader.Reader("manual_control process", (400,300), 380, 12, height=280, bg=(0,30,30), fgcolor=(255,255,255)), }
        [element.show() for element in self.text.values()]
        self.logger = multiprocessing.Queue()
        self.quitting = multiprocessing.Event()

        ### virtual obot setup ###
        self.bot = servo.Robot(dict(
                waist=servo.Servo(7, 900, 2100, 90, 3.2, 1),
                shoulder=servo.Servo(6, 600, 2400, 130, 5.75, 1),
                elbow=servo.Servo(5, 600, 2400, 110, 7.375, 1),
                wrist=servo.Servo(4, 600, 2400, 20, 3.5, 1),
                claw=servo.Servo(3, 600, 2400, 40, 0.0, 1),
            ), .1, self.bot_log)

        ### protocols setup ###
        self.manual = manual_control.Controller(self.bot, self.manual_control_log)

        self.automatic = automatic_control.Controller(self.bot, self.automatic_control_log)

        ### keys setup ###
        self.keymap = {
            #'return': (self.automatic.start, ()),
            #'space': (self.automatic.pause, ()),
            #'right arrow': (self.automatic.next, ()),
            #'left arrow': (self.automatic.last, ()), 
            '1': (self.manual.events.put, (('set_mode_individual', ()),)),
            '2': (self.manual.events.put, (('set_mode_blank', ()),)),
            '3': (self.manual.events.put, (('set_mode_test', ()),)),
            'space': (self.automatic.input.put, (('toggle_pause', ()),)),
            'left': (self.automatic.input.put, (('last', ()),)),
            'right': (self.automatic.input.put, (('next', ()),)),
            'e': (lambda self: self.bot_log(str(self.bot)), (self, )),
            'escape': (pygame.quit, ()),
        }

         ### stuff ###
        self.master_log('setup!')
        self.i = 0
        self.delay(0)
        self.run()

    def run(self):
        self.master_log('looping...')
        while not self.quitting.is_set():
            if not self.is_delayed():
                self.test()
            for current_event in event.get():
                self.event(current_event)
            while not self.logger.empty():
                category, msg = self.logger.get()
                self.text[category].TEXT += msg
                self.text[category].show()
        print ('quits')
        self._quit()

    def is_delayed(self):
        return self.delay_time > time.time()

    def delay(self, period):
        self.delay_time = time.time() + period

    def event(self, event):
        if event.type == pygame.QUIT:
            self.quit()
        elif event.type == pygame.KEYDOWN:
            self.keys(event)
        else:
            self.unknown(event)

    def unknown(self, event):
        self.master_log('Unkown event: ' + str(event))

    def keys(self, event):
        try:
            (func, args) = self.keymap[key.name(event.key)]
        except KeyError:  # print out unknown key
               (func, args) = (self.master_log, ('Unmapped key: %s' % key.name(event.key),))
        self.master_log(func.__name__ + ' ' + str(args))
        func(*args)

    def log(self, category, msg):
        try:
            self.text[category]
        except KeyError:
            self.log('master', 'unknown category: ' + category + ' is broadcasting: ' + msg)
        else:
            self.logger.put((category, '\n' + msg))

    def master_log(self, msg):
        self.log('master', msg)

    def bot_log(self, msg):
        self.log('bot', msg)

    def automatic_control_log(self, msg):
        self.log('automatic_control', msg)

    def manual_control_log(self, msg):
        self.log('manual_control', msg)

    def test(self):
        if self.i == 0:
            self.i = 1
            self.delay(.2)
        elif self.i < 10:
            self.delay(1)
            self.master_log('%i' % self.i)
            self.i += 1
        else:
            return

    def quit(self):
        if not self.quitting.is_set():
            self.quitting.set()
            self.master_log('quitting')
        else:
            self.master_log('already quit')

    def _quit(self):
            self.manual.quit()
            self.automatic.quit()
            self.bot.quit()
            pygame.quit()


if __name__ == '__main__':
    app = None
    try:
        app = App()
    except:
        print ('error')
        raise
        app.quit()