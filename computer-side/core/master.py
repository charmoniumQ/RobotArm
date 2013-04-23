import functools
import sys
import os
import time
from core import robot, automatic_control, manual_control
from framework import four_panel, util
from config import robot_setup, logs

f = functools.partial


class App(four_panel.FourPanel):
    def __init__(self):
        self.init_tk()
        self.init_processes()
        self.init_keys()

    def init_tk(self):
        four_panel.FourPanel.__init__(self)
        self.root.bind('<Key>', self.key)
        self.root.bind('<Button-1>', self.mouse)
        self.root.focus_set()
        self.set(0, 0, 'Master\n')
        self.set(0, 1, 'Robot\n')
        self.set(1, 0, 'Auto controls\n')
        self.set(1, 1, 'Manual controls\n')

    def init_processes(self):
        self.log = f(self.append, 0, 0)
        self.bot = robot.Robot(robot_setup.servos, f(self.append, 0, 1))
        self.auto = automatic_control.AutomaticControl(self.bot,
            f(self.append, 1, 0), self.quit)
        self.manual = manual_control.ManualControl(self.bot,
            f(self.append, 1, 1), self.quit)

        self.bot.start()
        self.auto.start()
        self.manual.start()

        print 'robot %d' % self.bot.pid
        print 'automatic controls %d' % self.auto.pid
        print 'manual controls%d' % self.manual.pid
        print 'master %d' % os.getpid()

    def init_keys(self):
        self.key_map = {
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
        #TODO: investigate quitting cleanly
        print 'quits'
        try:
            self.bot.quit()
        except:
            print 'robot', sys.exc_info()
        try:
            self.auto.quit()
        except:
            print 'automatic controls', sys.exc_info()
        try:
            self.manual.quit()
        except:
            print 'manual controls', sys.exc_info()
        try:
            four_panel.FourPanel.quit(self)
        except:
            print sys.exc_info()
        print 'quitted'

    @staticmethod
    def execute():
        f = App()
        f.mainloop()
        f.quit()

if __name__ == '__main__':
    App.execute()
