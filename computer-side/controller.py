from __future__ import print_function
import process


class Controller(process.Process):
    def __init__(self, bot, log_function=print):
        process.Process.__init__(self, log_function)
        self.bot = bot
