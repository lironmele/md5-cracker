import BaseAscii

class Range:
    def __init__(self, start='aaaaaa', stop='zzzzzz', range_count=10):
        self.start = BaseAscii.BaseAscii(start)
        self.stop = BaseAscii.BaseAscii(stop)
        self.range_count = range_count
        self.ranges = self / self.range_count

    def __div__(self, x):
        pass
