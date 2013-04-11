from framework import controller
from framework import executor

# OHNO! ITS DIAMOND INHERITANCE!
class AutomaticControl(executor.ExecutorProcess, controller.ControllerProcess):
    def __init__(self, bot, logger):
        controller.ControllerProcess.__init__(self, bot, logger)
        executor.ExecutorProcess.__init__(self, logger, [], False)
        # that was easy.