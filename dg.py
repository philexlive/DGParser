from enum import Enum
import re
import sys
import pathlib
import unittest

class Tk(Enum):
    OPEN_ARROW=0
    CLOSE_ARROW=1
    AT_OPERATOR=2
    ASSIGN_OPERATOR=3
    SLASH_OPERATOR=4
    INTEGER_LITERAL=5
    FLOAT_LITERAL=6
    BOOL_LITERAL=7
    STRING_LITERAL=8
    IDENTIFIER=9


class LexicalAnalyzer:

    class TokenizerState(Enum):
        INITIAL=0
        FINISH=1
        READING_ID_OR_KEY=2
        READING_NUMBER=3
        READING_STRING=4

        

    def tokenize(self, tokens, file):
        
        def is_letter(s):
            if re.fullmatch(r"^[a-zA-Z]", s):
                return True
            return False

        def is_digit(s): 
            if re.fullmatch(r"^\d$", s):
                return True
            return False

        def is_dot(s):
            return s == '.'

        def is_quote(s):
            return s == '"'

        def is_operator(s):
            return s in ['<','>','@','=','/']

        def is_delimiter(s):
            return s in [' ', '\n', '\t', '<', '>', '@', '=', '/', '']


        def check_operator(s):
            return {'<': Tk.OPEN_ARROW,
                    '>': Tk.CLOSE_ARROW,
                    '@': Tk.AT_OPERATOR,
                    '=': Tk.ASSIGN_OPERATOR,
                    '/': Tk.SLASH_OPERATOR }[s]

        def check_number(s):
            if re.fullmatch(r"^[-+]?\d+$", s):
                return Tk.INTEGER_LITERAL
            elif re.fullmatch(r"^[-+]?(\d+|\d*\.\d+)$", s):
                return Tk.FLOAT_LITERAL
            
            raise SyntaxError(f"Unexpected literal {s}.")

        def check_id_or_key(s):
            pattern = re.compile(r"^(true|false)$", re.IGNORECASE)
            if pattern.fullmatch(s):
                return Tk.BOOL_LITERAL
            return Tk.IDENTIFIER

        St = self.TokenizerState

        state = St.INITIAL
        buffer = ''
        while state != St.FINISH:
            c = file.read(1)

            match state:
                case St.INITIAL:
                    if is_delimiter(c):
                        if is_operator(c):
                            tokens.append((check_operator(c), c))
                    elif is_letter(c):
                        buffer += c
                        state = St.READING_ID_OR_KEY
                    elif is_digit(c) or is_dot(c):
                        buffer += c
                        state = St.READING_NUMBER
                    elif is_quote(c):
                        state = St.READING_STRING

                case St.READING_ID_OR_KEY:
                    if is_delimiter(c):
                        tokens.append((check_id_or_key(buffer), buffer))

                        if is_operator(c):
                            tokens.append((check_operator(c), c))
                            
                        buffer = ''
                        state = St.INITIAL
                    else:
                        buffer += c
                
                case St.READING_NUMBER:
                    if is_delimiter(c):
                        tokens.append((check_number(buffer), buffer))

                        if is_operator(c):
                            tokens.append((check_operator(c), c))

                        buffer = ''
                        state = St.INITIAL
                    elif is_letter(c):
                        raise SyntaxError(f"Unexpected literal {buffer}.")
                    else:
                        buffer += c
                
                case St.READING_STRING:
                    if is_quote(c):
                        tokens.append((Tk.STRING_LITERAL, buffer))
                        buffer = ''
                        state = St.INITIAL
                    else:
                        buffer += c
            if c == '':
                state = St.FINISH


args = sys.argv
if len(args) > 1:
    path = pathlib.Path(sys.argv[1])

    if path.is_file():
        with open(path, encoding="utf-8") as f:
            tokens = []
            LexicalAnalyzer().tokenize(tokens, f)
            for tk in tokens:
                print(tk)
