from __future__ import print_function
import process


class ControllerProcess(process.Process):
    def __init__(self, bot, log_function, call_super=True):
        '''This is the superclass of processes that talk to/give instructions to the bot

        (mostly just for organization. Not much real code, except for managing robot)
        bot is the roboot.Robot instance,
        log_function will be called with logs,
        call_super will tell me weather or not to call process.Process.__init__
        (helps with some weird diamond inheritance problems'''
        if call_super:  # helps handle diamond inheritance
            process.Process.__init__(self, log_function)
        self.bot = bot

    def _quit(self):
        self.bot.quit()
        process.Process.quit(self)
