from enum import Enum
from abc import ABC


class State(ABC):
    pass

class Init(State):
    def __init__(self, path):
        self.path = path

class Delimit(State):
    def __init__(self, file, substr,  pointer, tokens):
        self.file = file
        self.substr = substr
        self.pointer = pointer
        self.tokens = tokens

class Tokenize(State):
    def __init__(self, data):
        self.data = data

class Parse(State):
    def __init__(self, data):
        self.data = data

class Finish(State):
    def __init__(self, msg):
        self.msg = msg


class Wrapper:
    def __init__(self, state):
        self.state = state


class Tk(Enum):
    OPEN_PAREN=0
    CLOSE_PAREN=1
    IDENTIFIER=2
    LITERAL=3
    OPERATOR=4

    FINISH={'message': ''}



def analyze(path):
    wr = Wrapper(Init(path))

    while True:
        match wr.state:
            case Init():
                initialize(wr)
            case Delimit():
                delimit(wr)
            case Tokenize():
                tokenize(wr)
            case Parse():
                wr.state = Finish('Finished successful')
            case _:
                break


def initialize(wr):
    file = open(wr.state.path, encoding="utf-8")

    if file:
        wr.state = Delimit(file, '', 0, [])
        return

    message = ("Finishied unsuccessful, " 
               "file couldn\'t open")
    wr.state = Finish(message)


def is_separator(s):
    return s in [' ', '\n', '\t']


def delimit(wr):
    st = wr.state

    while True:
        c = st.file.read(1)
        cursor = st.file.tell()

        if not is_separator(c):
            wr.state.substr += c

        if is_separator(c) and st.pointer == cursor-1:
            wr.state.pointer = cursor
        elif is_separator(c) and st.pointer != cursor-1:
            wr.state.tokens.append(st.substr)
            wr.state.pointer = cursor
            wr.state.substr = ''

        if c == '':
            wr.state.file.close()
            wr.state = Tokenize(st.tokens) 
            break



def tokenize(wr):
    print(wr.state.data)
    wr.state = Parse([])

analyze("res.phyobj")
analyze("res1.phyobj")
