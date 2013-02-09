import pygame
from pygame import event
from pygame import joystick
from pygame import display
import sys
import servo

UP = 1
DOWN = -1


class ManualController(object):
    def __init__(self):
        pygame.init()
        self.screen = display.set_mode((100, 100))
        event.set_blocked([pygame. ACTIVEEVENT, pygame.KEYUP,
            pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN,
            pygame.JOYBALLMOTION, pygame.JOYHATMOTION, pygame.JOYBUTTONUP,
            pygame.VIDEORESIZE, pygame.VIDEOEXPOSE, pygame.USEREVENT])
        if joystick.get_count():
            self.controls = joystick.Joystick(0)
        else:
            raise BaseException('No joystick detected. Please reconect it.')
        self.controls.init()

        self.bot = servo.Robot(dict(
                waist=servo.Servo(7, 400, 900+1500, 60, 3.2),
                shoulder=servo.Servo(6, 600, 2400, 86, 5.75),
                elbow=servo.Servo(5, 600, 2400, 0, 7.375),
                wrist=servo.Servo(4, 600, 2400, 0, 3.5),
                claw=servo.Servo(3, 600, 2400, 0, 0)
            ), [5, 15, 25])

        self.coords = [0, 0, 0, 0]
        self.speed = -2

    def loop(self):
        self.update()
        for current_event in event.get():
            self.event(current_event)

    def event(self, current_event):
        if current_event.type == pygame.QUIT:
            self.quit(current_event)
        if current_event.type == pygame.JOYBUTTONDOWN:
            self.buttons(current_event)
        if current_event.type == pygame.KEYDOWN:
            self.keys(current_event)

    def quit(self, current_event):
        pygame.quit()
        sys.exit()

    def update(self):
        self.bot['waist'].aug(self.get_axis(2) * 1.2)
        self.bot['shoulder'].aug(self.get_axis(3) * -0.9)
        self.bot['elbow'].aug(self.get_axis(1) * 1.2)
        self.bot['wrist'].aug(self.controls.get_hat(0)[1] * 1.7 * 1.5**self.speed)

    def get_axis(self, axis):
        return round((self.controls.get_axis(axis) * 1.5**self.speed * 5) / 5, 1)

    def buttons(self, current_event):
        #print ('Button %i down' % current_event.button)
        if current_event.button == 6:
            self.sensitivity(DOWN)
        if current_event.button == 7:
            self.sensitivity(UP)
        if current_event.button == 5:
            self.bot['claw'].set(0)
        if current_event.button == 4:
            self.bot['claw'].set(180)
        if current_event.button == 1:
            event.post(event.Event(pygame.QUIT, method='joystick x button'))

    def sensitivity(self, increment):
        self.speed += increment
        print (round(1.5**self.speed * 50, 1))

    def keys(self, current_event):
        print (current_event.key)
        if current_event.key == pygame.K_ESCAPE:
            event.post(event.Event(pygame.QUIT, method='escape key'))
        if current_event.key == pygame.K_e:
            for name, servo in self.bot.servos.items():
                print ('%s: %i degrees' % (name, servo.read()))


def main():
    app = ManualController()
    print ('ready')
    while True:
        app.loop()

if __name__ == '__main__':
    main()
