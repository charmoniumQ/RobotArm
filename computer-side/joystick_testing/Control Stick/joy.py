import math
import pygame

import helpers

class SimulatedJoystick (object):
    def __init__(self, joyI):
        self.stick = pygame.joystick.Joystick(joyI)

    def __getattr__(self, name):
        if hasattr(self.stick, name):
            return getattr(self.stick, name)
        else:
            raise AttributeError ('pygame joystick does not have the attribute: ' + name)

    def get_axis(self, n):
        try:
            return self.get_axis(n)
            print ('real one')
        except:
            return 0

    def get_button(self, i):
        return False

class Joystick:
    def __init__(self):
        pygame.joystick.init()
        numJoys = pygame.joystick.get_count()
        if not numJoys:
            raise Exception ('Noy Joystick detected')
        joyI = 0
        self.joystick = SimulatedJoystick(joyI)
        self.joystick.init()

        self.numButtons = self.joystick.get_numbuttons()
        self.buttons = [0]*self.numButtons

        self.x = 0
        self.y = 0
        self.rad = 0

        pygame.font.init()
        self.font = pygame.font.Font('CRYSRG__.TTF',32)

    def compute(self):
        self.x = self.joystick.get_axis(0)
        self.y = self.joystick.get_axis(1)
        self.rad = math.hypot(self.x,self.y)
        self.rad = helpers.limitToRange(self.rad,0,1)
        self.ang = math.atan2(self.y,self.x)
        self.x = self.rad*math.cos(self.ang)
        self.y = self.rad*math.sin(self.ang)
        #'clicks' to middle
        tab = .12
        if -tab < self.x < tab:
            self.x = 0
        if -tab < self.y < tab:
            self.y = 0

        for i in xrange(self.numButtons):
            self.buttons[i] = self.joystick.get_button(i)

    def draw(self,surface):
        r = 200
        w = surface.get_width()
        h = surface.get_height()

        for i in xrange(self.numButtons):
            if self.buttons[i]:
                col = (0,255,0)
            else:
                col = (64,0,64)
            text = self.font.render(str(i),1,col)
            surface.blit(text,text.get_rect(centerx=w*(i+1)/(self.numButtons+1),centery=h/2))
        
        x = int(round(w/2+self.x*r))
        y = int(round(h/2+self.y*r))
        pygame.draw.aaline(surface,(128,128,128),(w/2,h/2),(x,y),1)
        pygame.draw.circle(surface,(0,0,0),(x,y),8,4)
        pygame.draw.circle(surface,(0,255,255),(w/2,h/2),r,2)

        
            
        
        
