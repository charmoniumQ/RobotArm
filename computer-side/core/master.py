import functools
import sys
import os
import multiprocessing
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
        '''Organized place for __init__-ing tk things'''
        four_panel.FourPanel.__init__(self)
        self.after(100, self.main)
        self.root.bind('<Key>', self.key)
        self.root.bind('<Button-1>', self.mouse)
        self.root.focus_set()
        self.set(0, 0, 'Master\n')
        self.set(0, 1, 'Robot\n')
        self.set(1, 0, 'Auto controls\n')
        self.set(1, 1, 'Manual controls\n')

    def init_processes(self):
        '''Organized place for __init__-ing process things'''
        self.log_msg = multiprocessing.Queue()

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
        '''Organized place for __init__-ing key things'''
        self.key_map = {
            'left': self.auto.last,
            'right': self.auto.next,
            'space': self.auto.pause,
        }

    def main(self):
        '''Logs things in the log queue'''
        while not self.log_msg.empty():
            args = self.log_msg.get()
            try:
                self.append(*args)
            except TypeError:
                print (args)

    def request_log(self, row, col, msg):
        '''Asks nicely to post a log to the master's 4-panel logger.'''
        self.log_msg.put((row, col, msg))

    def key(self, event):
        '''Processes a key event.

        logs:
        logs.core['master']['key']
            Gives event data
        logs.core['master']['unmapped_key']
            In the case that there is no action associated with the key,
            This will log.
        logs.core['master']['do_key']
            This is what the program is executing'''
        if logs.core['master']['key']:
            print ('pressed key: {ev.char} {ev.keysym} {ev.keycode}'
                .format(ev=event))
        key = event.keysym
        try:
            func = self.key_map[key]
        except KeyError:  # print out unknown key
            if logs.core['master']['unmapped_key']:
                func = f(util.printf, ('Unmapped key: %s' % key))
            else:
                func = util.passf
        else:
            if logs.core['master']['do_key']:
                print ('Key: {k}, doing {f!s}'
                       .format(k=key, f=func))
        func()

    def mouse(self, event):
        '''Processes a mouse event'''
        if logs.core['master']['mouse']:
            print ('clicked at: {ev.x}, {ev.y}'.format(ev=event))

    def quit(self):
        '''Please call this when done.
        
        Appendages like manual_control can call this when they want to.
        (useful if you want to be able to quit out of this through a joystick button'''
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
