from __future__ import print_function
import time
from core import robot

s = robot.Robot('F', print, [('left', 1, 10, 100, 0),
                       ('right', 2, 10, 100, 0),
                       ('front', 3, 200, 1000, 50), ])
s.start()
s.action_input('print(str(self))')
s.indirect_move('left', 60)
s.action_input('print(str(self))')
time.sleep(2)
s.indirect_move('right', 60)
s.action_input('print(str(self))')
time.sleep(2)
s.indirect_move('front', 60)
s.action_input('print(str(self))')
while not s.idle():
    pass
s.quit()
