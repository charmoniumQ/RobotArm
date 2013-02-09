from __future__ import print_function
import time
import pygame
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
        self.quitting = False
        print ('pygame setup!')

        ### virtual obot setup ###
        self.bot = servo.Robot(dict(
                waist=servo.Servo(7, 900, 2100, 90, 3.2, 1),
                shoulder=servo.Servo(6, 600, 2400, 130, 5.75, 1),
                elbow=servo.Servo(5, 600, 2400, 110, 7.375, 1),
                wrist=servo.Servo(4, 600, 2400, 20, 3.5, 1),
                claw=servo.Servo(3, 600, 2400, 40, 0.0, 1),
            ), .1)
        self.bot.process = multiprocessing.Process(target=runner, args=(self, 'bot'))
        self.bot.process.start()

        ### protocols setup ###
        class Struct(object):
            pass
        manual = Struct()
        manual.run = self.manual.run
        self.manual = manual_control.Controller(self.bot)
        self.manual.process = multiprocessing.Process(target=runner, args=(self, 'manual'))
        self.manual.process.start()

        self.automatic = automatic_control.Controller(self.bot)
        self.automatic.process = multiprocessing.Process(target=runner, args=(self, 'automatic'))
        self.automatic.process.start()

        ### keys setup ###
        self.keymap = {
            #'return': (self.automatic.start, ()),
            #'space': (self.automatic.pause, ()),
            #'right arrow': (self.automatic.next, ()),
            #'left arrow': (self.automatic.last, ()), 
            '1': (self.manual.set_mode, (self.manual.blank, )),
            '2': (self.manual.set_mode, (self.manual.individual, )),
            '3': (self.manual.set_mode, (self.manual.blank, )),
            'e': (lambda self: print(self.bot), (self, )),
            'escape': (pygame.quit, ()),
        }

        ### stuff ###
        print ('ready-- looping')
        self.loop()

    def loop(self):
        self.test()
        while not self.quitting:
            for current_event in event.get():
                self.event(current_event)
            try:
                event.pump()
            except pygame.error:
                return # pygame has already quit
        self.quit()

    def event(self, event):
        if event.type == pygame.QUIT:
            self.quit()
        elif event.type == pygame.KEYDOWN:
            self.keys(event)
        else:
            self.unknown(event)

    def unknown(self, event):
        print ('Unkown event: ' + str(event))

    def keys(self, event):
        try:
            (func, args) = self.keymap[key.name(event.key)]
        except KeyError:  # print out unknown key
               (func, args) = (print_function, 'Unmapped key: %s' % key.name(event.key))
        print ('master: ' + str(func) + ' ' + str(args))
        func(*args)

    def test(self):
        time.sleep(0)
        for ctr in range(5):
            time.sleep(1.5)
            print ('master: %i' % ctr)

    def quit(self):
        if self.quitting == False:
            print ('quits')
            self.quitting = True
            self.manual.quit()
            self.automatic.quit()
            self.bot.quit()
            pygame.quit()
        else:
            print ('already quit')


if __name__ == '__main__':
    app = App()
    #app.quit()
