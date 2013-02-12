from __future__ import print_function
import multiprocessing
import time
import collections


class Controller (multiprocessing.Process):
    def __init__(self, robot):
        self.bot = robot
        self.input = Multiprocessing.Queue()
        self.index = 0
        self.commands = [ ( 'blank', () ),
                          ( 'test', () ), ] #  preprogrammed routine
        self.quitting = multiprocessing.Event()
        self.i = 0
        super(Controller, self).__init__()

    def run(self):
        print ('automatic control looping...')
        while not self.quitting.is_set():
            while not self.input.empty():
                self.commands.insert(idx + 1, self.input.get())
                #  put the realtime input ahead of all of the preprogrammed routine
            if index != len(commands):
                index += 1
                func, args = commands[index]
                func = getattr(self, func)
                func(*args)

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

    #def change(self, change_type):  # FIXME
    #    self.input.put(change_type)
    #
    #def start(self):
    #    self.pause = False
    #
    #def stop(self):
    #    self.pause = True
    #
    ##def last(self):  # FIXME: do more than just last function
    ##    self.commands.queue.appendleft(self.last)
    #
    ##def next(self):
    ##    self.commands.queue.popleft()
    #
    #def delay(self, duration):  # FIXME
    #    self.timedone = get current time + duration
    #    if get current time > self.timedone:
    #        self.pause = True
    #    else:
    #        self.pause = False
    #    queue.put_left(self.delay,)

    def quit(self):  # FIXME
        self.quitting.set()
        self.bot.quit()
