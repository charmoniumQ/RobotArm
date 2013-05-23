from framework import controller
from framework import executor

# OHNO! ITS DIAMOND INHERITANCE!
class AutomaticControl(executor.ExecutorProcess, controller.ControllerProcess):
    def __init__(self, bot, logger, quit_super):
        '''This class is the junction of an ExecutorProcess and a ControllerProcess

        bot is an instance of robot
        logger is a logging funcion
        quit_super will be called when this program quits,
        useful if you want to let this appendage call the quit of a larger system,
        when this appendage is done.'''
        controller.ControllerProcess.__init__(self, bot, logger)
        executor.ExecutorProcess.__init__(self, logger, [], False)
        self.quit_super = quit_super

    def _quit(self):
        '''See documentation for  process.Process._quit'''
        print ('automatic control quitting')
        controller.ControllerProcess.quit(self)
        executor.ExecutorProcess.quit(self)
        self.quit_super()
        # that was easy.