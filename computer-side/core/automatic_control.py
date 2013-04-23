from framework import controller
from framework import executor

# OHNO! ITS DIAMOND INHERITANCE!
class AutomaticControl(executor.ExecutorProcess, controller.ControllerProcess):
    def __init__(self, bot, logger, quit_super):
        controller.ControllerProcess.__init__(self, bot, logger)
        executor.ExecutorProcess.__init__(self, logger, [], False)
        self.quit_super = quit_super

    def _quit(self):
        print ('automatic control quitting')
        controller.ControllerProcess.quit(self)
        executor.ExecutorProcess.quit(self)
        self.quit_super()
        # that was easy.