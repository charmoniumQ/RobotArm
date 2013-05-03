import functools
import sys
import os
import multiprocessing
from core import robot, automatic_control, manual_control
from framework import four_panel, util
from config import robot_setup, logs

f = functools.partial
REFRESH_MILLIS = 350


class App(four_panel.FourPanel):
    def __init__(self):
        self.init_tk()
        self.init_processes()
        self.init_keys()
        print ('started')

    def init_tk(self):
        four_panel.FourPanel.__init__(self)
        self.root.bind('<Key>', self.key)
        self.root.bind('<Button-1>', self.mouse)
        self.root.focus_set()
        self.set(0, 0, 'Master\n')
        self.set(0, 1, 'Robot\n')
        self.set(1, 0, 'Auto controls\n')
        self.set(1, 1, 'Manual controls\n')
        self.log_msg = multiprocessing.Queue()
        self.main()

    def init_processes(self):
        self.log = f(self.request_log, 0, 0)
        self.bot = robot.Robot(robot_setup.servos, f(self.request_log, 0, 1))
        self.auto = automatic_control.AutomaticControl(self.bot,
            f(self.request_log, 1, 0), self.quit)
        self.manual = manual_control.ManualControl(self.bot,
            f(self.request_log, 1, 1), self.quit)

        self.bot.start()
        self.auto.start()
        self.manual.start()
        self.log(str(os.getpid()))

    def init_keys(self):
        self.key_map = {
            'left': self.auto.last,
            'right': self.auto.next,
            'space': self.auto.pause,
        }

    def main(self):
        self.after(REFRESH_MILLIS, self.main)
        while not self.log_msg.empty():
            args = self.log_msg.get()
            try:
                self.append(*args)
            except TypeError:
                print (args)

    def request_log(self, row, col, msg):
        self.log_msg.put((row, col, msg))

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
            print 'master', sys.exc_info()
        print 'quitted'

    @staticmethod
    def execute():
        f = App()
        f.mainloop()
        f.quit()

if __name__ == '__main__':
    App.execute()
