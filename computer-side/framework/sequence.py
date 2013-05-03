
class Sequence(object):
    def __init__(self, data, majors):
        if not len(data) == len(majors):
            raise ValueError('Data and majors need to be the same size')
        self.data = data
        self.majors = majors
        self.index = -1

    def __next__(self):
        self.index += 1
        return self.data[self.index]

    def skip(self, direction=0):
        self.index = self.majors.find(True, self.index + direction)

    def left(self, direction=-1):
        self.skip(direction)

    def right(self, direction=1):
        self.skip(direction)