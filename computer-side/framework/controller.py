from __future__ import print_function
import re
import process
from config import logs


r = re.compile('self\._servos\[{wildcard}\]\.{wildcard}\({wildcard}\)'
               .format(wildcard='(.*?)'))


class ControllerProcess(process.Process):
    def __init__(self, bot, log_function):
        process.Process.__init__(self, log_function)
        self.bot = bot
        if logs.framework['controller']['__init__']:
            self.log('Controller setup successfully!')

    def run(self):
        pass

    def _do_action(self, action):
        self.log('hi1')
        if logs.framework['controller']['command']:
            f = r.match(action)
            self.log('hi2')
            self.log('%s %s to %s' % f.groups())
        process.Process._do_action(self, action)

    def quit(self):
        self.bot.quit()
        process.Process.quit(self)
