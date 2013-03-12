from __future__ import print_function
import time
from core import robot
from config import robot_setup

bot = robot.Robot(robot_setup.servos, print)
print (str(bot))
bot.start()

for angle in range(0, 181, 30):
    bot.indirect_move('elbow', angle)
    time.sleep(1.5)
    print (str(bot))

bot.quit()
