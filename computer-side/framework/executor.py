from __future__ import print_function
import process
from config import logs


class ExecutorProcess (process.Process):
    def __init__(self, log_function, routine=None):
        process.Process.__init__(self, log_function)
        if routine is None:
            if logs.framework['executor']['__init__']:
                self.log('Blank routine')
            self.routine = []
        else:
            if logs.framework['executor']['__init__']:
                self.log('Existing routine')
            self.routine = routine
        self.index = 0

    def mode(self):
        while self.index != len(self.routine):
            process.Process.mode(self)

    def _mode(self):
        if logs.framework['executor']['_mode']:
            self.log('Doing action #%d' % self.index)
        action = self.routine[self.index]
        self.do_action(action)
        self.next()

    def skip(self, delta_index):
        if logs.framework['executor']['skipping']:
            self.log('Skipping to action #%d' % self.index + delta_index)
        self.index += delta_index

    def next(self, delta_index=1):
        self.skip(delta_index)

    def last(self, delta_index=-1):
        self.skip(delta_index)
