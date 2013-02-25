from __future__ import print_function
import time
import pygame
import sys
import multiprocessing
from pygame import display
from pygame import event
from pygame import key
import servo
import manual_control
import automatic_control


class App(object):
    def __init__(self):
        ### pygame setup ###
        pygame.init()
        self.screen = display.set_mode((100, 100))
        event.set_blocked([pygame. ACTIVEEVENT, pygame.KEYUP,
            pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN,
            pygame.JOYBALLMOTION, pygame.JOYHATMOTION, pygame.JOYBUTTONUP,
            pygame.VIDEORESIZE, pygame.VIDEOEXPOSE, pygame.USEREVENT,
            pygame.JOYAXISMOTION])
        pygame.register_quit(self.quit)
        self.quitting = multiprocessing.Event()
        print ('pygame: setup!')

        ### virtual obot setup ###
        self.bot = servo.Robot(dict(
                waist=servo.Servo(7, 900, 2100, 90, 3.2, 1),
                shoulder=servo.Servo(6, 600, 2400, 130, 5.75, 1),
                elbow=servo.Servo(5, 600, 2400, 110, 7.375, 1),
                wrist=servo.Servo(4, 600, 2400, 20, 3.5, 1),
                claw=servo.Servo(3, 600, 2400, 40, 0.0, 1),
            ), .1)

        ### protocols setup ###
        self.manual = manual_control.Controller(self.bot)

        self.automatic = automatic_control.Controller(self.bot)

        ### keys setup ###
        self.keymap = {
            #'return': (self.automatic.start, ()),
            #'space': (self.automatic.pause, ()),
            #'right arrow': (self.automatic.next, ()),
            #'left arrow': (self.automatic.last, ()), 
            '1': (self.manual.events.put, (('set_mode_individual', ()),)),
            '2': (self.manual.events.put, (('set_mode_blank', ()),)),
            '3': (self.manual.events.put, (('set_mode_test', ()),)),
            'e': (lambda self: print(self.bot), (self, )),
            'escape': (pygame.quit, ()),
        }

         ### stuff ###
        print ('master: looping...')
        self.i = 0
        super(App, self).__init__()
        self.run()

    def run(self):
        while not self.quitting.is_set():
            self.test()
            for current_event in event.get():
                self.event(current_event)
        self._quit()

    def event(self, event):
        if event.type == pygame.QUIT:
            self.quit()
        elif event.type == pygame.KEYDOWN:
            self.keys(event)
        else:
            self.unknown(event)

    def unknown(self, event):
        print ('master: Unkown event: ' + str(event))

    def keys(self, event):
        try:
            (func, args) = self.keymap[key.name(event.key)]
        except KeyError:  # print out unknown key
               (func, args) = (print_function, 'Unmapped key: %s' % key.name(event.key))
        print ('master: ' + str(func) + ' ' + str(args))
        func(*args)

    def test(self):
        if self.i == 0:
            time.sleep(0)
            self.i = 1
        elif self.i < 5:
            time.sleep(1)
            print ('master: %i' % self.i)
            self.i += 1
        else:
            return

    def quit(self):
        if not self.quitting.is_set():
            self.quitting.set()
            print ('master: quitting')
        else:
            print ('master: already quit')

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
        app.quit()
        print ('error')
        raise