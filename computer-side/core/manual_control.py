from framework import controller, joystick
from config import logs


class ManualControl(controller.ControllerProcess, joystick.JoystickReader):
    def __init__(self, bot, logger_function):
        controller.ControllerProcess.__init__(self, bot, logger_function)
        joystick.JoystickReader.__init__(self, logger_function)
        self._mode = self.blank

    def run(self):
        controller.ControllerProcess.run(self)

    def blank(self):
        pass

    def adjust_axis(self, name, axis):  # TODO: scale by time elapsed
        val = self.controls.get_axis(axis)
        if logs.core['manual_control']['movement']:
            if val:
                print (val)
        return self.bot.get_sensitivity(name) * val

    def joystick(self):
        #self.bot.direct_augment("waist", self.adjust_axis("waist", 5))
        self.bot.direct_augment("shoulder", self.adjust_axis("shoulder", 2))
        self.bot.direct_augment("elbow", self.adjust_axis("elbow", 0))
        #self.bot.direct_augment("wrist", self.adjust_axis("wrist", 6))
        #self.bot.direct_augment("claw", self.adjust_axis("claw", 4))
        if self.controls.get_button(4):
            self.bot.sens_s_down()
        if self.controls.get_button(5):
            self.bot.sens_s_down()

    def _actually_do_action(self, action):
        controller.ControllerProcess._actually_do_action(self, action)

    def set_mode(self, mode):
        if logs.core['manual_control']:
            self.log(mode)
        self._mode = getattr(self, mode)

    def get_mode(self):
        return self._mode

    #TODO: fancy property function decorator elegance
    mode = property(get_mode, set_mode)

    def quit(self):
        controller.ControllerProcess.quit(self)
        joystick.JoystickReader(self)