from __future__ import print_function
import multiprocessing
import time
import collections


class Controller (multiprocessing.Process):
    def __init__(self, robot):
        self.bot = robot
        self.input = multiprocessing.Queue()
        self.index = 0
        self.commands = [ ( 'blank', () ),
                          ( 'test', () ), 
                          ( 'test', () ), 
                          ( 'test', () ), 
                          ( 'test', () ), 
                          ( 'test', () ), ] #  preprogrammed routine
        self.quitting = multiprocessing.Event()
        self.begin()
        self.i = 0
        print ('automatic_control: setup!')
        super(Controller, self).__init__()
        self.start()

    def run(self):
        print ('automatic_control: looping...')
        while not self.quitting.is_set():
            while not self.input.empty():
                self.commands.insert(idx + 1, self.input.get())
                #  put the realtime input ahead of all of the preprogrammed routine
            if not (self.is_paused() or self.is_delayed()):
                self.index += 1
                func, args = None, None
                try:
                    func, args = self.commands[self.index]
                except IndexError:
                    pass
                else:
                    func = getattr(self, func)
                    func(*args)
        self._quit()

    def blank():
        #  this function is needed at self.commands[0]
        #  as a dummy function to pad the preprogramed routine,
        #  as well as a failsafe, so that if the user trys to go 'last' to many times,
        #  we just execute self.commands[0] (no negative numbers).
        pass

    def test(self):
        if self.i == 0:
            time.sleep(.4)
            self.i = 1
        elif self.i < 5:
            time.sleep(1)
            print ('automatic control: %i' % self.i)
            self.i += 1
        else:
            return

    def is_delayed(self):
        return self.delay_time > time.time()

    def delay(self, period):
        self.delay_time = time.time() + period

    def pause(self, status):
        print ('automatic_control: pause' + str(status))
        self.pause = status

    def is_paused(self):
        return self.pause

    def begin(self):
        self.pause(False)
        self.delay(0)

    def stop(self):
        self.pause(True)

    def skip(self, delta_index):
        self.index += delat_index
    
    def next(self, delta_index=1):
        self.skip(delta_index)

    def last(self, delta_index=-1):
        self.skeip(delta_index)

    def quit(self):
        self.quitting.set()

    def _quit(self):
        self.bot.quit()
        self.input.close()