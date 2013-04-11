import time
from core import robot
from config import robot_setup

def printy(arg):
    print (arg)


bot = robot.Robot(robot_setup.servos, printy)
print (str(bot))
bot.start()

for angle in range(0, 181, 30):
    bot.indirect_move('elbow', angle)
    time.sleep(1.5)
    print (str(bot))

bot.quit()
