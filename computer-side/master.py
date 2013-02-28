import time
import sys
import os
import inspect
import multiprocessing
import pygame
from pygame import display
from pygame import event
from pygame import key
from pygame import mouse
import reader
import servo
import manual_control
import automatic_control

TRAILING_SPACE = 2

class Struct (object):
    pass


class App(object):
    def __init__(self):
        ### pygame setup ###
        pygame.init()
        self.screen = display.set_mode((800, 800))
        display.set_caption('Control a Robotic Arm!')
        event.set_blocked([pygame.ACTIVEEVENT, pygame.KEYUP,
            pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN,
            pygame.JOYBALLMOTION, pygame.JOYHATMOTION, pygame.JOYBUTTONUP,
            pygame.VIDEORESIZE, pygame.VIDEOEXPOSE, pygame.USEREVENT,
            pygame.JOYAXISMOTION])
        pygame.register_quit(self.quit)
        self.buffers = {}
        self.text = {'master': reader.Reader("master process", (10,10), 380, 10, height=380, bg=(10,30,60), fgcolor=(255,255,255)),
                     'bot': reader.Reader("bot process", (400,10), 380, 10, height=380, bg=(10,30,60), fgcolor=(255,255,255)),
                     'automatic_control': reader.Reader("automatic_control process", (10,400), 380, 10, height=380, bg=(10,30, 60), fgcolor=(255,255,255)),
                     'manual_control': reader.Reader("manual_control process", (400,400), 380, 10, height=380, bg=(10,30,60), fgcolor=(255,255,255)), }
        for name, element in self.text.items():
            self.buffers[name] = Struct()
            self.buffers[name].element = element
            self.buffers[name].element.show()
            self.buffers[name].buffer = ['output of ' + name + ': ']
            self.buffers[name].pos = 0
            self.buffers[name].autoscroll = True
        del self.text # replaced by self.buffers
        self.logger = multiprocessing.Queue()
        self.quitting = multiprocessing.Event()

        ### virtual obot setup ###
        self.bot = servo.Robot(dict(
                waist=servo.Servo(7, 900, 200, 90, 3.2, 1),
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
            '1': (self.manual_input, ('set_mode_individual',)),
            '2': (self.manual_input, ('set_mode_blank',)),
            '3': (self.manual_input, ('set_mode_test',)),
            'space': (self.automatic_input, ('toggle_pause',)),
            'left': (self.automatic_input, ('last',)),
            'right': (self.automatic_input, ('next', )),
            'e': (self.bot_input, ('log_pos',)),
            'escape': (pygame.quit, ()),
            'i': (self.scroll_mouse_up, ()),
            'k': (self.scroll_mouse_down, ()),
            'b': (self.auto_scroll_toggle_mouse, ()),
            'down': (lambda: 0, ()),
            'up': (lambda: 0, ()),
        }
        self.silent_events = ['i', 'k', 'down', 'up']
        key.set_repeat(110, 50)
        
         ### stuff ###
        self.master_log('setup!')
        self.i = 0
        self.delay(0)
        self.run()

    def run(self):
        self.master_log('looping...')
        self.bot_log(str(self.bot))
        while not self.quitting.is_set():
            if not self.is_delayed():
                self.test()
            for current_event in event.get():
                self.event(current_event)
                for log in self.buffers.values():
                    log.element.update(current_event)
            event.pump()
            while not self.logger.empty():
                category, msg = self.logger.get()
                log = self.buffers[category]
                log.buffer.append(msg)
            for name, log in self.buffers.items():
                self._auto_scroll(name)
                log.element.TEXT = '\n'.join(log.buffer[log.pos:])
                log.element.show()
        print ('quits')
        self._quit()

    def manual_input(self, function, *args):
        self.manual.events.put((function, args))

    def automatic_input(self, function, *args):
        self.automatic.input.put((function, args))

    def bot_input(self, function, *args):
        self.bot.queue.put((function, args))

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
        if key.name(event.key) not in self.silent_events:
            self.master_log(func.__name__ + ' ' + str(args))
        func(*args)

    def scroll(self, category, delta):
        self.buffers[category].pos += delta
        if self.buffers[category].pos < 0:
            self.buffers[category].pos = 0
        if self.buffers[category].pos > len(self.buffers[category].buffer) - TRAILING_SPACE:
            self.buffers[category].pos = len(self.buffers[category].buffer) - TRAILING_SPACE

    def scroll_up(self, category, delta=-1):
        self.scroll(category, delta)

    def scroll_down(self, category, delta=1):
        self.scroll(category, delta)

    def _auto_scroll(self, category):
        log = self.buffers[category]
        if log.autoscroll:
            while len(log.buffer) - log.pos > log.element.height / (1.3*log.element.FONTSIZE) - TRAILING_SPACE:
                self.scroll_down(category)
        

    def auto_scroll(self, category, b):
        self.buffers[category].autoscroll = b
        self.log(category, 'Autoscroll? ' + str(b))
        if b:
            self.buffers[category].element.BG = (10, 30, 60)
        else:
            self.buffers[category].element.BG = (10, 30, 30)
        self.buffers[category].element.show()

    def auto_scroll_on(self, category):
        self.auto_scroll(cateory, True)

    def auto_scroll_off(self, category):
        self.auto_scroll(cateory, False)

    def auto_scroll_toggle(self, category):
        self.auto_scroll(category, (not self.buffers[category].autoscroll))

    def auto_scroll_toggle_mouse(self):
        self.auto_scroll_toggle(self.get_mouse())

    def get_mouse(self):
        x, y = mouse.get_pos()
        if x <= 400 and y <= 400:
            return 'master'
        if x > 400 and y <= 400:
            return 'bot'
        if x <= 400 and y > 400:
            return 'automatic_control'
        if x > 400 and y > 400:
            return 'manual_control'

    def scroll_mouse_up(self):
        self.scroll_up(self.get_mouse())

    def scroll_mouse_down(self):
        self.scroll_down(self.get_mouse())

    def log(self, category, msg):
        try:
            self.buffers[category]
        except KeyError:
            self.log('master', 'unknown category: ' + category + ' is broadcasting: ' + msg)
        else:
            self.logger.put((category, msg))

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
    os
    app = None
    try:
        app = App()
    except:
        print ('error')
        raise
        app.quit()