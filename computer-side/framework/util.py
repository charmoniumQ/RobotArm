import functools
import time
import Tkinter as tk
from framework import process

# python's keywords are not being functions,
# and that annoys me... (not a good thing)
def printf(args):
    print args

def passf():
    pass

def execf(string, local):
    exec(string, local)

def mapi(val, in_min, in_max, out_min, out_max):
    '''Much like arduino's map function.

if val is on a scale between in_min and in_max, 
then the return value is the proportional value on a scale between
out_min and out_max'''
    return int((float(val) - in_min) / (in_max - in_min) * 
               (out_max - out_min) + out_min)


class Logger(process.Process):
    def __init__(self):
        process.Process.__init__(self, functools.partial(self.write, 'App'))

    def _write(self, name, msg):
        print '%s: %s' % (name, msg)

    def write(self, name, msg):
        self.do_action('self._write({0!r}, {1!r})'.format(name, msg))

    def test(self, s):
        pass

    def logobot(self, s):
        self.write('Robot', s)

    def logAuto(self, s):
        self.write('Auto', s)

    def logManual(self, s):
        self.write('Manual', s)


class GUIProcess(tk.Frame):
    def __init__(self, root=None):
        if root is None:
            root = tk.Tk()
        self.root = root
        tk.Frame.__init__(self, self.root)

    #TODO: quit cleanly
    def quit(self):
        self.root.quit()
        try:
            self.root.destroy()  # For environments like IDLE
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