class BaseAscii:
    def __init__(self, string):
        self.string = string
        self.base26_list = self._to_ascii()
        self.number = self._base_10_to_26()
    
    def _to_ascii(self):
        return list(map(lambda c: ord(c) - 97, self.string))

    def _base_10_to_26(self):
        base10 = 0
        n = len(self.base26_list) - 1

        for i in self.base26_list:
            base10 += i * 26**n
            n -= 1

        return base10

    def __sub__(self, x):
        if self.number > x.number:
            return self.number - x.number + 1
        else:
            return x.number - self.number + 1

    def __gt__(self, x):
        return self.number > x.number

    def __lt__(self, x):
        return self.number < x.number

def main():
    start = BaseAscii("aaa")
    stop = BaseAscii("bbd")

    print(start-stop)

if __name__ == "__main__":
    main()
