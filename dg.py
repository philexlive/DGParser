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


class Tk(Enum):
    OPEN_PAREN=0
    CLOSE_PAREN=1
    IDENTIFIER=2
    LITERAL=3
    OPERATOR=4

    FINISH={'message': ''}


def analyze(path):
    state = Init(path)

    while True:
        match state:
            case Init():
                state = initialize(state)
            case Delimit():
                state = delimit(state)
            case Tokenize():
                state = tokenize(state)
            case Parse():
                state = Finish('Finished successful')
            case _:
                break


def initialize(state):
    file = open(state.path, encoding="utf-8")

    if file:
        return Delimit(file, '', 0, [])

    message = ("Finishied unsuccessful, " 
               "file couldn\'t open")
    return Finish(message)


def is_separator(s):
    return s in [' ', '\n', '\t']


def delimit(st):
    c = st.file.read(1)
    cursor = st.file.tell()

    if not is_separator(c):
        st.substr += c

    if is_separator(c) and st.pointer == cursor-1:
        st.pointer = cursor
    elif is_separator(c) and st.pointer != cursor-1:
        st.tokens.append(st.substr)
        st.pointer = cursor
        st.substr = ''

    if c == '':
        st.file.close()
        return Tokenize(st.tokens) 

    return st


def tokenize(st):
    print(st.data)
    return Parse([])

analyze("res.phyobj")
analyze("res1.phyobj")
