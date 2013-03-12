from __future__ import print_function
from framework import executor


class Test(executor.ExecutorProcess):
    def __init__(self):
        self.msg = 'Hello, World'
        executor.ExecutorProcess.__init__(self, print, [
            'print("hi")',
            'self.delay(1)',
            'print("hello")',
            'self.delay(1)',
            'print("hey")',
            'self.delay(1)',
            'print(self.msg)',
            'self.quit()'
            ])


if __name__ == '__main__':
    print ('running')
    f = Test()
    f.start()
    while not f.idle():
        pass
