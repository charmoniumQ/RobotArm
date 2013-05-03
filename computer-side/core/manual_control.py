from core import simple_joy
from framework import controller


class ManualControl(controller.ControllerProcess):
    def __init__(self, bot, logger_function, quit_super):
        controller.ControllerProcess.__init__(self, bot, logger_function)
        self.quit_super = quit_super

    def _mode(self):
        self.controls._mode()

    def setup(self):
        self.controls = simple_joy.Runner(self.bot, self.log, self.quit_super)
        controller.ControllerProcess.setup(self)

    def _quit(self):
        print ('manual control quitting')
        self.controls.quit()
        controller.ControllerProcess.quit(self)
        self.quit_super()
