import functools
import Tkinter as tk
from core import robot, automatic_control, manual_control
from framework import util
from config import robot_setup
from config import logs

f = functools.partial


class App(util.GUIProcess):
    def __init__(self):
        util.GUIProcess.__init__(self)
        self.frame = tk.Frame(self.master, width=640, height=480,
            takefocus=1)
        self.frame.bind('<Key>', self.key)
        self.frame.bind('<Button-1>', self.mouse)
        self.frame.grid()
        self.frame.focus_set()

        self.log = util.Logger()
        self.bot = robot.Robot(robot_setup.servos, self.log.logobot)
        self.auto = automatic_control.AutomaticControl(self.bot,
            self.log.logAuto)
        self.manual = manual_control.ManualControl(self.bot,
            self.log.logManual)

        self.log.start()
        self.bot.start()
        self.auto.start()
        self.manual.start()

        self.key_map = {'e': f(util.execf, 'util.print(str(self.bot))', locals()),
            '1': f(self.manual.set_mode, 'blank'),
            '2': f(self.manual.set_mode, 'joystick'),
            'left': self.auto.last,
            'right': self.auto.next,
            'space': self.auto.pause,
        }

    def key(self, event):
        if logs.core['master']['key']:
            print ('pressed key: {ev.char} {ev.keysym} {ev.keycode}'
                .format(ev=event))
        self.do_key(event.keysym)

    def do_key(self, keysym):
        func = None
        try:
            func = self.key_map[keysym]
        except KeyError:  # print out unknown key
            if logs.core['master']['unmapped_key']:
                func = f(util.printf, ('Unmapped key: %s' % keysym))
            else:
                func = util.passf
        else:
            if logs.core['master']['do_key']:
                print ('Key: {k}, doing {f!s}'
                       .format(k=keysym, f=func))
        func()

    def mouse(self, event):
        if logs.core['master']['mouse']:
            print ('clicked at: {ev.x}, {ev.y}'.format(ev=event))

    def quit(self):
        try: self.bot.quit()
        except: pass
        try: self.auto.quit()
        except: pass
        try: self.manual.quit()
        except: pass
        try: util.GUIProcess.quit(self)
        except: pass
        while not self.log.idle():
            pass
        try: self.log.quit()
        except: pass

if __name__ == '__main__':
    App().run()
