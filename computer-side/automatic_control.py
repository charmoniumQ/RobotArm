from __future__ import print_function
import multiprocessing
import time


class Controller (multiprocessing.Process):
    def __init__(self, robot):
        self.bot = robot
        self.commands = multiprocessing.Queue()
        self.commands.put(('test', ()))
        self.pause = False
        self.delay = False
        self.quitting = False
        self.last = [('blank', ())]
        print ('automatic control setup!')

    def run(self):
        print ('automatic control looping...')
        while not self.quitting:
            while not self.commands.empty():
                if self.pause:
                    continue
                func, args = self.commands.get()
                func = getattr(self, func)
                func(*args)
                self.last.append((func, args))

    def blank():
        pass

    def test(self):
        time.sleep(4)
        for ctr in range(5):
            time.sleep(1.5)
            print ('automatic_control: %i' % ctr)

    def change(self, change_type):  # FIXME
        self.commands.put(change_type)

    def start(self):
        self.pause = False

    def stop(self):
        self.pause = True

    def last(self):  # FIXME: do more than just last function
        self.commands.queue.appendleft(self.last)

    def next(self):
        self.commands.queue.popleft()

    def delay(self, duration):  # FIXME
        time.sleep(duration)

    def quit(self):  # FIXME
        self.bot.quit()
