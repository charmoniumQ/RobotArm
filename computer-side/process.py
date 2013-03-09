import multiprocessing
import time
import sys


class Process (multiprocessing.Process):
    def __init__(self, log_function):
        multiprocessing.Process.__init__(self)

        self.log = log_function
        self.input = multiprocessing.Queue()
        self.quitting = multiprocessing.Event()
        self.delay(0)
        self.paused(False)

        self.log('Setup succesful!')

    def run(self):
        self.log('Looping...')
        self.loop()
        self._quit()

    def loop(self):
        while not self.quitting.is_set():
            self._loop()

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
        #self.log('Doing: ' + action)
        try:
            self._do_action(action)
        except:
            self.log('Could not execute: ' + action)
            info = sys.exc_info()[:-1]  # last msg ussually not useful
            for msg in info:
                self.log(str(msg))

    def _do_action(self, action):
        exec action in locals()

    #  TODO: figure out property business
    #@property
    def idle(self):
        return self.input.empty()

    #@property
    def is_delayed(self):
        return self.delay_time_millis > time.time()

    #@delay.setter
    def delay(self, period):
        self.delay_time_millis = time.time() + period

    #@property
    def paused(self, status):
        self.log('paused? ' + str(status))
        self.paused = status

    #@paused.setter
    def is_paused(self):
        return self.paused

    def action_input(self, action):
        #self.log('Will do: ' + action)
        self.input.put(action)

    #@property
    def is_quitting(self):
        return self.quitting.is_set()

    #@is_quitting.setter
    def quit(self):
        if not self.quitting.is_set():
            self.log('Quitting...')
            self.quitting.set()
        else:
            self.log('Already quit')

    def _quit(self):
        self.input.close()

    def __del__(self):  # TODO: is del'ing necessary?
        try:
            self.quit()
        except:  # already partially destructed
            self._quit()
