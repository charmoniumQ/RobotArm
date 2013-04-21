from core import simple_joy
from framework import controller
from config import logs


class ManualControl(controller.ControllerProcess):
    def __init__(self, bot, logger_function):
        controller.ControllerProcess.__init__(self, bot, logger_function)
        self.controls = simple_joy.Runner(bot)
        self.state = self.blank

    def _mode(self):
        self.controls._mode()

    def quit(self):
        self.controls.quit()
        controller.ControllerProcess.quit(self)