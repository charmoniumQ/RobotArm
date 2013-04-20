from __future__ import print_function
import process


class ControllerProcess(process.Process):
    def __init__(self, bot, log_function, call_super=True):
        if call_super:  # helps handle diamond inheritance
            process.Process.__init__(self, log_function)
        self.bot = bot

    def _quit(self):
        self.bot.quit()
        process.Process.quit(self)
