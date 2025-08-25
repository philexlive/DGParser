class TokenIterator:
    def __init__(self, data):
        self.data = data
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index == len(self.data):
            raise StopIteration
        token = self.data[self.index]
        self.index += 1
        return token

dt = [1, 2, 3, 4]
ti = TokenIterator(dt)

print(next(ti))
print(next(ti))
print(next(ti))
print(next(ti))
print(next(ti))