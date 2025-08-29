class TokensStream:
    def __init__(self, data=None):
        if data is None:
            data = []

        self.data = data
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index == len(self.data):
            raise StopIteration
        item = self.data[self.index]
        self.index += 1
        return item

    def append(self, item):
        self.data.append(item)

    def reset(self):
        self.index = 0
