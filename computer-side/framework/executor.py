from __future__ import print_function
import process
from config import logs


class ExecutorProcess (process.Process):
    def __init__(self, log_function, routine=None, call_super=True):
        '''An executor is a process that has a routine,
and one can ask it to do the next item, do the last item, pause, skip items...

        log_function will be called with log messages
        routine is the default routine
        call_super is weather or not to call process.Process.__init__
        (fixes some weird diamond inheritance problem)

        logs:
        logs.framework['executor']['__init__']
            tells you if it got a routine'''
        if call_super:  # helps handle diamond inheritance
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
        '''See docs from process.Process.mode'''
        if self.index != len(self.routine):
            process.Process.mode(self)

    def _mode(self):
        '''See docs from process.Process._mode'''
        if logs.framework['executor']['_mode']:
            self.log('Doing action #%d' % self.index)
        action = self.routine[self.index]
        self.do_action(action)
        self.next()

    def skip(self, delta_index):
        '''skips the next delta_index items'''
        if logs.framework['executor']['skipping']:
            self.log('Skipping to action #%d' % self.index + delta_index)
        self.index += delta_index

    def next(self, delta_index=1):
        '''goes to next item'''
        self.skip(delta_index)

    def last(self, delta_index=-1):
        '''goes to last item'''
        self.skip(delta_index)
