from __future__ import print_function
import time
from core import robot

s = robot.Robot( [('left', 1, (600, 2400), 10),
                   ('right', 2, (600, 2400), 50),
                   ('front', 3, (600, 2400), 100), ],
                print)
s.start()
s.do_action('print(str(self))')
s.indirect_move('left', 60)
s.do_action('print(str(self))')
time.sleep(2)
s.indirect_move('right', 60)
s.do_action('print(str(self))')
time.sleep(2)
s.indirect_move('front', 60)
s.do_action('print(str(self))')
while not s.idle():
    pass
s.quit()
