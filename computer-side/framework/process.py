import multiprocessing
import time
import sys
from config import logs


class Process (multiprocessing.Process):
    def __init__(self, log_function):
        multiprocessing.Process.__init__(self)
        self.log = log_function
        self.input = multiprocessing.Queue()
        self.quitting = multiprocessing.Event()
        self.delay(0)
        self.paused(False)
        if logs.framework['process']['__init__']:
            self.log('Setup succesful')

    def run(self):
        if logs.framework['process']['run']:
            self.log('Begining to loop')
        self.loop()
        self._quit()

    def loop(self):
        while not self.is_quitting():
            self._loop()
            if logs.framework['process']['loop']:
                self.log('Finished loop')

    def _loop(self):
        self.process_input()
        self.mode()

    def process_input(self):
        while not self.input.empty():
            self._process_input()

    def _process_input(self):
        action = self.input.get()
        self.do_action(action)

    def mode(self):
        if not (self.is_paused() or self.is_delayed()):
            self._mode()

    def _mode(self):
        pass

    def do_action(self, action):
        if logs.framework['process']['do_action']:
            self.log('Doing: ' + action)
        try:
            self._do_action(action)
        except:
            if logs.framework['process']['error']:
                self.log('Could not execute: ' + action)
            info = sys.exc_info()[:-1]  # last msg usually not useful
            for msg in info:
                if logs.framework['process']['error']:
                    self.log(str(msg))

    def _do_action(self, action):
        exec action in locals()

    #  TODO: figure out property business
    #@property
    def idle(self):
        if logs.framework['process']['idle'] and self.input.empty():
            self.log('Idle')
        return self.input.empty()

    #@property
    def is_delayed(self):
        return self.delay_time_millis > time.time()

    #@delay.setter
    def delay(self, period):
        self.delay_time_millis = time.time() + period

    #@property
    def paused(self, status):
        if logs.framework['process']['paused']:
            self.log('paused? ' + str(status))
        self.paused1 = status

    #@paused.setter
    def is_paused(self):
        return self.paused1

    def action_input(self, action):
        if logs.framework['process']['action_input']:
            self.log('Will do: ' + action)
        if logs.framework['process']['idle'] and self.idle():
            self.log('Not idle')
        self._action_input(action)

    def _action_input(self, action):
        self.input.put(action)

    #@property
    def is_quitting(self):
        return self.quitting.is_set()

    #@is_quitting.setter
    def quit(self):
        if not self.quitting.is_set():
            if logs.framework['process']['quit']:
                self.log('Quitting...')
            self.quitting.set()
        else:
            if logs.framework['process']['double_quit']:
                self.log('Already quit')

    def _quit(self):
        try:
            self.input.close()
        except:
            pass  # already destructed

    def __del__(self):  # TODO: is del'ing necessary?
        try:
            self.quit()
        except:  # already partially destructed
            self._quit()
