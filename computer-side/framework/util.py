import functools
import time
import Tkinter as tk
from framework import process

# python's keywords are not being functions,
# and that annoys me... (not a good thing)
def printf(args):
    '''function form of the print statement'''
    print args

def passf():
    '''function form of the pass statement'''
    pass

def execf(string, local):
    '''function form of the exec statement'''
    exec(string, local)

def clamp(num, mn, mx):
    '''clamps num to a range between mn and mx inclusive'''
    return max(mn, min(num, mx))


class Logger(process.Process):
    def __init__(self):
        '''A new process that handles logging to stdout'''
        process.Process.__init__(self, functools.partial(self.write, 'App'))

    def _write(self, name, msg):
        '''The method used to log a msg from the process named name.

        override this if you want.'''
        print '%s: %s' % (name, msg)

    def write(self, name, msg):
        '''Requests that this process log msg from name politely.'''
        self.do_action('self._write({0!r}, {1!r})'.format(name, msg))

    def logobot(self, s):
        self.write('Robot', s)

    def logAuto(self, s):
        self.write('Auto', s)

    def logManual(self, s):
        self.write('Manual', s)


class GUIProcess(tk.Frame):
    def __init__(self, master=None):
        if master is None:
            master = tk.Tk()
        self.root = master
        tk.Frame.__init__(self, self.root)

    #TODO: quit cleanly
    def quit(self):
        try:
            self.master.destroy()  # For environments like IDLE
        except tk.TclError:
            pass

class Timer(object):
    def __init__(self, duration=0):
        self.delay(duration)

    #TODO: property swag
    def is_delayed(self):
        return self.delay_time_millis > time.time()

    def delay(self, period):
        self.delay_time_millis = time.time() + period

class FileLogger(object):
    def __init__(self, name):
        self.file = open(name, 'a')
        self.header()

    def header(self):
        self.log('\n\n')
        self.log(time.ctime())
        self.log('-'*79)

    def write(self, msg):
        self.file.write(msg)

    def log(self, msg):
        self.write(msg)
        self.write('\n')

    def close(self):
        self.file.close()

    def __del__(self):
        self.close()
