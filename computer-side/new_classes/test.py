from __future__ import print_function
import time
import executor

def blank(*args, **kwargs):
    pass

class Test(executor.Process):
    def __init__(self):
        executor.Process.__init__(self, print, [
                                         'print("hi")',
                                         'self.delay(1)',
                                         'print("hello")',
                                         'self.delay(1)',
                                         'print("hey")',
                                         'self.delay(1)',
                                         'self.quit()'
                                         ])


if __name__ == '__main__':
    print ('running')
    f = Test()
    f.start()
    time.sleep(3)