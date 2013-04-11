from __future__ import print_function
import re
import process
from config import logs


r = re.compile('self\._servos\[{wildcard}\]\.{wildcard}\({wildcard}\)'
               .format(wildcard='(.*?)'))


class ControllerProcess(process.Process):
    def __init__(self, bot, log_function, call_super=True):
        if call_super:  # helps handle diamond inheritance
            process.Process.__init__(self, log_function)
        self.bot = bot

    def _actually_do_action(self, action):
        # TODO: the following is a load of crap
        if logs.framework['controller']['command']:
            joy = r.match(action)
            if joy is not None:
                self.log('%s %s to %s' % joy.groups())
        process.Process._actually_do_action(self, action)

    def _quit(self):
        self.bot.quit()
        process.Process.quit(self)
