import process

class Process (process.Process):
    def __init__(self, log_function, routine=None):
        process.Process.__init__(self, log_function)
        if routine is None:
            self.routine = []
        else:
            self.routine = routine
        self.index = 0

    def mode(self):
        while self.index != len(self.routine):
            process.Process.mode(self)

    def _mode(self):
        action = self.routine[self.index]
        self.do_action(action)
        self.next()

    def skip(self, delta_index):
        self.index += delta_index

    def next(self, delta_index=1):
        self.skip(delta_index)

    def last(self, delta_index=-1):
        self.skip(delta_index)