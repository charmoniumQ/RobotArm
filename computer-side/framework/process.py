import multiprocessing
#import Queue
import time
import sys
from config import logs


class Process (multiprocessing.Process):
    def __init__(self, log_function, parallel=True):
        #TODO: modular
        multiprocessing.Process.__init__(self)
        self.log = log_function
        self.parallel = parallel
        self.actions_q = multiprocessing.Queue()
        self.quitting = multiprocessing.Event()
        self.delay(0)
        self.pause(False)
        if logs.framework['process']['__init__']:
            self.log('Setup succesful')

    def start(self):
        if not self.parallel:
            raise RuntimeError('This is thread is not set to run' +
                               'in self.parallel.')
        if self.is_alive():
            if logs.framework['process']['double_start']:
                self.log('Already started')
            return
        else:
            if logs.framework['process']['start']:
                self.log('Begining to loop')
            multiprocessing.Process.start(self)

    def run(self):
        self.setup()
        self.loop()
        self.end()

    def setup(self):
        self.loop_count = 0

    def loop(self):
        while not self.is_quitting():
            self._loop()
            self.loop_count += 1
            if logs.framework['process']['loop']:
                self.log('Finished loop %d' % self.loop_count)

    def _loop(self):
        self.process_queue()
        self.mode()

    def process_queue(self):
        while not self.actions_q.empty():
            action = self.actions_q.get()
            if logs.framework['process']['actions']:
                self.log('Doing: %s' % action)
            try:
                self._do_action(action)
            except:
                self.error(action, sys.exc_info())

    def _do_action(self, action):
        exec action in locals()

    def error(self, action, exc_info):
        if logs.framework['process']['error']:
            self.log('Could not execute: ' + action)
            self.log('Error type: %s' % exc_info[0])
            self.log('Error value: %s' % exc_info[1])

    def mode(self):
        if not (self.is_paused() or self.is_delayed()):
            self._mode()
        else:
            if logs.framework['process']['mode']:
                self.log('paused or delayed')

    def _mode(self):
        pass

    #  TODO: figure out property business
    #@property
    def idle(self):
        if logs.framework['process']['idle'] and self.actions_q.empty():
            self.log('Idle')
        return self.actions_q.empty()

    #@property
    def is_delayed(self):
        return self.delay_time_millis > time.time()

    #@delay.setter
    def delay(self, period):
        self.delay_time_millis = time.time() + period

    #@property
    def pause(self, status=None):
        if status == None:
            return self.pause(not self.is_paused())
        if logs.framework['process']['pause']:
            self.log('paused? ' + str(status))
        self.paused = status

    #@pause.setter
    def is_paused(self):
        return self.paused

    def do_action(self, action):
        if logs.framework['process']['do_action']:
            self.log('Will do: %s' % action)
        if logs.framework['process']['idle'] and self.idle():
            self.log('Not idle')
        if self.parallel:
            self.actions_q.put(action)
        else:
            self._do_action(action)

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
        try: self.actions_q.close()
        except: pass  # already destructed
        try: self.objects_q.close()
        except: pass

    def end(self):
        self._quit()

    def __del__(self):  # TODO: is del'ing necessary?
        try:
            self.quit()
        except:  # already partially destructed
            self._quit()
