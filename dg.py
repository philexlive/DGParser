from enum import Enum
from abc import ABC


class Tk(Enum):
    OPEN_PARAMS=0
    CLOSE_PARAMS=1
    CLOSE_BODY=2
    GROUP_NAME=3
    IDENTIFIER=4
    ASSIGN_OP=5
    LITERAL=6


def analyze(path):
    lexemes = []
    with open(path, encoding="utf-8") as file:
        delimit(lexemes, file)

    print(lexemes)


def delimit(lexemes, file):
    def is_separator(s):
        return s in [' ', '\n', '\t']

    pointer, cursor = 0, 0
    buffer = ''
    while True:
        c = file.read(1)
        cursor = file.tell()

        if not is_separator(c):
            buffer += c

        if is_separator(c) and pointer == (cursor - 1):
            pointer = cursor
        elif is_separator(c) and pointer != (cursor - 1):
            lexemes.append(buffer)
            pointer = cursor
            buffer = ''

        if c == '':
            break


import re

class Tokenizer:
    
    _is_delimiter = lambda self, s: s in [' ', '\n', '\t']
    _is_at_operator = lambda self, s: s == '@'
    _is_assign_operator = lambda self, s: s == '='
    _is_opening = lambda self, s: s == '<'
    _is_closing = lambda self, s: s == '>'
    _is_slash = lambda self, s: s == '/'
    _is_quote = lambda self, s: s == '"'
    _is_digit = lambda self, s: re.match(r"[0-9]", s) != None 
    _is_letter = lambda self, s: re.match(r"[a-zA-Z]", s) != None

    class State(Enum):
        INITIAL=0
        OPEN_ARROW=1
        CLOSE_ARROW=2
        CLOSE_BODY=3
        AT_OPERATOR=4
        ASSIGN_OPERATOR=5
        GROUP_NAME=6
        IDENTIFIER=7
        LITERAL=8
        QUOTE=9

    def tokenize(self, tokens, file):
        
        St = self.State

        def append_tk(tk, st=St.INITIAL, bf='', p_st=St.INITIAL):
            nonlocal state
            nonlocal buffer
            nonlocal prev_st
            tokens.append(tk)
            state = st
            buffer = bf
            prev_st = p_st


        state = St.INITIAL
        buffer = ''
        prev_st = state
        while True:
            c = file.read(1)

            match state:
                case St.INITIAL:
                    if self._is_opening(c):
                        state = St.OPEN_ARROW
                    elif self._is_closing(c) and buffer != '':
                        append_tk((Tk.CLOSE_BODY, buffer))
                    elif self._is_closing(c):
                        append_tk((Tk.CLOSE_PARAMS,))
                    elif self._is_at_operator(c):
                        state = St.GROUP_NAME
                    elif self._is_letter(c) and prev_st == St.ASSIGN_OPERATOR:
                        state = St.LITERAL
                    elif self._is_digit(c) and prev_st == St.ASSIGN_OPERATOR:
                        state = St.LITERAL
                    elif self._is_quote(c) and prev_st == St.ASSIGN_OPERATOR:
                        buffer = c
                        state = St.QUOTE
                    elif self._is_letter(c):
                        buffer = c
                        state = St.IDENTIFIER
                    elif self._is_assign_operator(c):
                        tokens.append((Tk.ASSIGN_OP,))
                        state = St.ASSIGN_OPERATOR
                
                case St.OPEN_ARROW:
                    if self._is_digit(c):
                        raise SyntaxError(buffer)
                    elif self._is_letter(c):
                        buffer += c
                    elif self._is_slash(c):
                        state = St.CLOSE_BODY
                    elif self._is_delimiter(c):
                        append_tk((Tk.OPEN_PARAMS, buffer))
                    elif self._is_at_operator(c):
                        append_tk((Tk.OPEN_PARAMS, buffer), 
                                  st=St.GROUP_NAME)
                    else:
                        buffer += c

                case St.GROUP_NAME:
                    if self._is_delimiter(c):
                        append_tk((Tk.GROUP_NAME, buffer))
                    else:
                        buffer += c

                case St.CLOSE_BODY:
                    if self._is_closing(c):
                        tokens.append((Tk.CLOSE_BODY,))
                        state = St.INITIAL

                case St.IDENTIFIER:
                    if self._is_delimiter(c):
                        append_tk((Tk.IDENTIFIER, buffer))
                    elif self._is_assign_operator(c):
                        tokens.append((Tk.IDENTIFIER, buffer))
                        buffer = ''
                        state = St.ASSIGN_OPERATOR
                    else:
                        buffer += c
                
                case St.ASSIGN_OPERATOR:
                    if self._is_delimiter(c):
                        append_tk((Tk.ASSIGN_OP,), 
                                  p_st=St.ASSIGN_OPERATOR)
                    elif self._is_letter(c) or self._is_digit(c):
                        append_tk((Tk.ASSIGN_OP,),
                                  bf=c,
                                  st=St.LITERAL,
                                  p_st=St.ASSIGN_OPERATOR)
                    elif self._is_quote(c):
                        append_tk((Tk.ASSIGN_OP,),
                                  bf=c,
                                  st=St.QUOTE,
                                  p_st=St.ASSIGN_OPERATOR)
                    elif self._is_assign_operator(c):
                        raise SyntaxError("Second assign operator")


                case St.LITERAL:
                    if self._is_delimiter(c):
                        append_tk((Tk.LITERAL, buffer))
                    else:
                        buffer += c

                case St.QUOTE:
                    if self._is_quote(c):
                        append_tk((Tk.LITERAL, buffer))
                    else:
                        buffer += c

            if c == '':
                break


def parse(tokens):
    pass


analyze("res.phyobj")
analyze("res1.phyobj")
print()
tkz = Tokenizer()
tokens = []
with open('res.phyobj', encoding="utf-8") as f:
    tkz.tokenize(tokens, f)
    for tk in tokens:
        print(tk)

print()

tokens = []
with open('res1.phyobj', encoding="utf-8") as f:
    tkz.tokenize(tokens, f)
    for tk in tokens:
        print(tk)
