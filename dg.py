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
    def __init(self, data):
        self.data

class Parse(State):
    def __init(self, data):
        self.data

class Finish(State):
    pass

class Tk(Enum):
    OPEN_PAREN=0
    CLOSE_PAREN=1
    IDENTIFIER=2
    LITERAL=3
    OPERATOR=4

class St(Enum):
    INIT={'path': ''}
    DELIMIT={'file':None, 'substr':'', 'left':0, 'right':0, 'tokens':[]}
    TOKENIZE={'result': []}
    PARSE={'data': []}
    FINISH={'message': ''}


def is_separator(s):
    return s in [' ', '\n', '\t']

def analyze(path):
    state = St.INIT
    state.value['path'] = path

    while True:
        match state:
            case St.INIT:
                state = initialize(state)
            case St.DELIMIT:
                state = delimit(state)
                state = St.TOKENIZE
            case St.TOKENIZE:
                state = St.PARSE
            case St.PARSE:
                state = St.FINISH
            case _:
                print(state)
                break

def initialize(state):
    file = open(state.value['path'], encoding="utf-8")

    state = St.FINISH

    if file:
        state = St.DELIMIT
        state.value['file'] = file
        return state

    message = ("Finishied unsuccessful, " 
                   "file couldn\'t open")
    state.value['message'] = message 
    return state


def delimit(state):
    st = state.value
    file = st['file']
    c = file.read(1)
    if not is_separator(c):
        st['substr'] += c
        st['right'] = file.tell()

    if is_separator(c) and st['left'] == st['right']:
        st['right'] = file.tell()
        st['left'] = st['right']
    elif is_separator(c) and st['left'] != st['right']:
        st['tokens'].append(st['substr'])
        st['left'] = st['right']
        st['substr'] = ''

    if c == '':
        file.close()
        new_state = St.TOKENIZE
        new_state.value['result'] = st['tokens']
        return new_state

    return St.DELIMIT


analyze("res.phyobj")
