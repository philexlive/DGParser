from enum import Enum
from abc import ABC

class State(ABC):
    pass


class Init(State):
    def __init__(self, path):
        self.path = path

class Delimit(State):
    def __init__(self, file, substr, left, right, tokens):
        self.file = file
        self.substr = substr
        self.left = left
        self.right = right
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


def is_separator(s):
    return s in [' ', '\n', '\t']

def analyze(path):
    state = Init(path)

    while True:
        match state:
            case Init():
                print(state)
                state = initialize(state)
                print(state)
            case Delimit():
                state = delimit(state)
            case Tokenize():
                print(state)
                state = Parse(0)
            case Parse():
                print(state)
                state = Finish('Finished successful')
            case _:
                print(state)
                break

def initialize(state):
    file = open(state.path, encoding="utf-8")

    if file:
        return Delimit(file, '', 0, 0, [])

    message = ("Finishied unsuccessful, " 
                   "file couldn\'t open")
    return Finish(message)


def delimit(st):
    c = st.file.read(1)

    if not is_separator(c):
        st.substr += c
        st.right = st.file.tell()

    if is_separator(c) and st.left == st.right:
        st.right = st.file.tell()
        st.left = st.right
    elif is_separator(c) and st.left != st.right:
        st.tokens.append(st.substr)
        st.left = st.right
        st.substr = ''

    if c == '':
        st.file.close()
        return Tokenize(st.tokens) 

    return st


analyze("res.phyobj")
