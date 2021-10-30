import BaseAscii

class Range:
    def __init__(self, start='aaaaaa', stop='zzzzzz', range_count=10):
        self.start = BaseAscii.BaseAscii(start)
        self.stop = BaseAscii.BaseAscii(stop)
        self.range_count = range_count
        self.ranges = []
        if self.range_count != 1:
            # self.ranges = self.div(self.range_count)
            self.ranges = self // self.range_count

    def __str__(self) -> str:
        string = f"start: {self.start.string}, stop: {self.stop.string}, count: {self.range_count}"
        
        for r in self.ranges:
            string += f"\r\n\t{r}"

        return string

    def __floordiv__(self, x):
        ranges = []
        r = None
        start_part = None
        end_part = None
        count_per_part = (self.stop - self.start) // x

        for i in range(x-1):
            start_part = BaseAscii.BaseAscii(self.start+(i*count_per_part))
            stop_part = BaseAscii.BaseAscii(self.start+((i+1)*count_per_part))

            ranges.append(Range(start_part.string, stop_part.string, 1))

        start_part = BaseAscii.BaseAscii(self.start+((x-1)*count_per_part))
        stop_part = BaseAscii.BaseAscii(self.stop.string)

        ranges.append(Range(start_part.string, stop_part.string, 1))

        return ranges

def main():
    default = Range()
    print(default)

if __name__ == '__main__':
    main()