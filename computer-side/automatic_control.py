import multiprocessing
import time
import collections


class Controller (multiprocessing.Process):
    def __init__(self, robot, log):
        self.bot = robot
        self.log = log
        self.input = multiprocessing.Queue()
        self.index = 0
        self.commands = [ ( 'blank', () ),
                          ( 'delay', (.3,) ),
                          ( 'log', ('1',) ),
                          ( 'delay', (1,) ),
                          ( 'log', ('2',) ),
                          ( 'delay', (1,) ),
                          ( 'log', ('3',) ),
                          ( 'delay', (1,) ),
                          ( 'log', ('4',) ),
                          ( 'delay', (1,) ),
                          ( 'log', ('5',) ),
                          ( 'delay', (1,) ),
                          ( 'log', ('6',) ),
                          ( 'delay', (1,) ),
                          ( 'log', ('7',) ),
                          ( 'delay', (1,) ),
                          ( 'log', ('8',) ),
                          ( 'delay', (1,) ),
                          ( 'log', ('9',) ),] #  preprogrammed routine
        self.quitting = multiprocessing.Event()
        self.executing = multiprocessing.Lock()
        self.begin()
        self.log('setup!')
        super(Controller, self).__init__()
        self.start()

    def run(self):
        self.log('looping...')
        while not self.quitting.is_set():
            while not self.input.empty():
                func, args = None, None
                try:
                    func, args = self.input.get()
                except IndexError:
                    pass
                else:
                    func = getattr(self, func)
                    func(*args)
            if not (self.is_paused() or self.is_delayed()):
                self.executing.acquire()
                self.index += 1
                func, args = None, None
                try:
                    func, args = self.commands[self.index]
                except IndexError:
                    pass
                else:
                    func = getattr(self, func)
                    func(*args)
                self.executing.release()
        self._quit()

    def blank():
        #  this function is needed at self.commands[0]
        #  as a dummy function to pad the preprogramed routine,
        #  as well as a failsafe, so that if the user trys to go 'last' to many times,
        #  we just execute self.commands[0] (no negative numbers).
        pass

    def is_delayed(self):
        return self.delay_time > time.time()

    def delay(self, period):
        self.delay_time = time.time() + period

    def pause(self, status):
        self.log('paused? ' + str(status))
        self.paused = status

    def toggle_pause(self):
        if self.is_paused():
            self.pause(False)
        else:
            self.pause(True)

    def is_paused(self):
        return self.paused

    def begin(self):
        self.pause(False)
        self.delay(0)

    def stop(self):
        self.pause(True)

    def skip(self, delta_index):
        self.executing.acquire()
        self.index += delta_index
        self.executing.release()

    def next(self, delta_index=1):
        self.skip(delta_index)
        if self.commands[self.index - 1][0] in ['delay', 'pause']:  # skip through these
            self.next()

    def last(self, delta_index=-1):
        self.skip(delta_index)
        if self.commands[self.index - 1][0] in ['delay', 'pause']:  # skip through these
            self.last()

    def quit(self):
        self.quitting.set()

    def _quit(self):
        self.bot.quit()
        self.input.close()