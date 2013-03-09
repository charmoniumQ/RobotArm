from __future__ import print_function
import process


class ExecutorProcess (process.Process):
    def __init__(self, log_function=print, routine=None):
        process.Process.__init__(self, log_function)
        if routine is None:
            self.routine = []
        else:
            self.routine = routine
        self.index = 0

    def mode(self):
        while self.index != len(self.routine):
            process.Process.mode(self)

    def _mode(self):
        action = self.routine[self.index]
        self.do_action(action)
        self.next()

    def skip(self, delta_index):
        self.index += delta_index

    def next(self, delta_index=1):
        self.skip(delta_index)

    def last(self, delta_index=-1):
        self.skip(delta_index)


#from __future__ import print_function
#import time
#import executor
#
#def blank(*args, **kwargs):
#    pass
#
#class Test(executor.MyProcess):
#    def __init__(self):
#        executor.MyProcess.__init__(self, print, [
#                                         'print("hi")',
#                                         'self.delay(1)',
#                                         'print("hello")',
#                                         'self.delay(1)',
#                                         'print("hey")',
#                                         'self.delay(1)',
#                                         'self.quit()'
#                                         ])
#
#
#if __name__ == '__main__':
#    print ('running')
#    f = Test()
#    f.start()
#    time.sleep(3)