import time
from config import robot_setup

def east_goal(self):
    self.move_to({'waist':141.163,
                  'shoulder':95.351,
                  'elbow':146.684,
                  'wrist':41,
                  'claw':158.04,})

def north_goal(self):
    self.move_to({'waist':94.339,
                  'shoulder':118.826,
                  'elbow':121.568,
                  'wrist':66.48,
                  'claw':158.04,})

def west_goal(self):
    self.move_to({'waist':46.13100,
                  'shoulder':95.351,
                  'elbow':146.684,
                  'wrist':41,
                  'claw':158.04,})

def spare(self):
    self.move_to({'waist':70.246,
                  'shoulder':24.5,
                  'elbow':154.5,
                  'wrist':41,
                  'claw':0,})

def left_bonus(self):
    self.move_to({'waist':68.5,
                  'shoulder':128.596,
                  'elbow':97.539,
                  'wrist':83.233,
                  'claw':158,})

def right_bonus(self):
    self.move_to({'waist':122.5,
              'shoulder':128.94,
              'elbow':97.539,
              'wrist':97.55,
              'claw':158,})

def print_stuff(self):
    for name, servo in self.bot._servos.iteritems():
        self.log('sensitivity: %s at N^%.6f * %.6f' % (name, servo.sens_exp, servo.sens))
    self.log('sensitivity: robot at N^%.6f * %.6f' % (self.bot.sens_exp, self.bot.sens))
    self.log(self.bot)

def quitter(self):
    self.quit()

def home(self):
    #TODO: move beginning position to here.
    opts = dict((x[0],x[3]) for x in robot_setup.servos)
    self.move_to(opts)

def ready(self):
    self.move_to({'waist':    96.178,
                  'shoulder': 115.79,})
    time.sleep(0.4)
    self.move_to({'elbow':    162.116,
                  'wrist':    109.143,
                  'claw':     0,})
    time.sleep(0.4)
    self.move_to({'elbow':    162.116,})

joystick_buttons = {
    0: east_goal,
    1: north_goal,
    2: west_goal,
    3: spare,
    4: left_bonus,
    5: right_bonus,
    6: print_stuff,
    7: quitter,
}

keyboard = {
    'q': quitter,
}