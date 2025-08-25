from enum import Enum
import re
import sys
import pathlib
from html.parser import starttagopen


class Tk(Enum):
    OPEN_ARROW=0
    CLOSE_ARROW=1
    ASSIGN_OPERATOR=3
    SLASH_OPERATOR=4
    INTEGER_LITERAL=5
    FLOAT_LITERAL=6
    BOOL_LITERAL=7
    STRING_LITERAL=8
    IDENTIFIER=9
    

class Tokenizer:

    class St(Enum):
        INITIAL=0
        FINISH=1
        READING_ID_OR_KEY=2
        READING_NUMBER=3
        READING_STRING=4


    def tokenize(self, tokens, file):
        St = self.St
        

        is_delimiter = self.is_delimiter
        is_operator = self.is_operator
        is_letter = self.is_letter
        is_digit = self.is_digit
        is_quote = self.is_quote
        is_dot = self.is_dot

        check_operator = self.check_operator
        check_number = self.check_number
        check_id_or_key = self.check_id_or_key
        
        
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


    def is_letter(self, s):
        if re.fullmatch(r"^[a-zA-Z]", s):
            return True
        return False

    def is_digit(self, s): 
        if re.fullmatch(r"^\d$", s):
            return True
        return False

    def is_dot(self, s):
        return s == '.'

    def is_quote(self, s):
        return s == '"'

    def is_operator(self, s):
        return s in ['<', '>', '=', '/']

    def is_delimiter(self, s):
        return s in [' ', '\n', '\t', '<', '>', '=', '/', '']


    def check_operator(self, s):
        return {'<': Tk.OPEN_ARROW,
                '>': Tk.CLOSE_ARROW,
                '=': Tk.ASSIGN_OPERATOR,
                '/': Tk.SLASH_OPERATOR }[s]

    def check_number(self, s):
        if re.fullmatch(r"^[-+]?\d+$", s):
            return Tk.INTEGER_LITERAL
        elif re.fullmatch(r"^[-+]?(\d+|\d*\.\d+)$", s):
            return Tk.FLOAT_LITERAL
            
        raise SyntaxError(f"Unexpected literal {s}.")

    def check_id_or_key(self, s):
        pattern = re.compile(r"^(true|false)$", re.IGNORECASE)
        if pattern.fullmatch(s):
            return Tk.BOOL_LITERAL
        return Tk.IDENTIFIER


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


class Node:
    pass

class ValueNode(Node):
    def __init__(self):
        self.value = ''

class AttrNode(Node):
    def __init__(self, name):
        self.name = name

class StatementNode(Node):
    def __init__(self):
        self.statements = []

class DefinitionNode(Node):
    def __init__(self):
        self.statements = []
        self.nodes = []


class Parser:

    def __init__(self, tki):
        self.tki = tki
        self.sym = ''
        self._next_sym()

    def _next_sym(self):
        try:
            self.sym = next(self.tki)
        except StopIteration:
            return

    def _accept(self, sym):
        if self.sym[0] == sym:
            self._next_sym()
            return True
        return False

    def _expect(self, sym):
        if self._accept(sym):
            return
        raise SyntaxError('Unexpected symbol')


    def statement(self):
        self._expect(Tk.ASSIGN_OPERATOR)
        print('attr', end=' ')
        if self._accept(Tk.STRING_LITERAL):
            print('= string')
        elif self._accept(Tk.INTEGER_LITERAL):
            print('= integer')
        elif self._accept(Tk.FLOAT_LITERAL):
            print('= float')
        elif self._accept(Tk.BOOL_LITERAL):
            print('= bool')
        else:
            raise SyntaxError('Unexpected symbol or object disclosed')

    def expect_closing(self):
        if self._accept(Tk.SLASH_OPERATOR):
            self._expect(Tk.CLOSE_ARROW)
            return True
        return False

    def definition(self):
        self._expect(Tk.IDENTIFIER)

        while self._accept(Tk.IDENTIFIER):
            self.statement()

        if self.expect_closing():
            return

        self._expect(Tk.CLOSE_ARROW)

        while self._accept(Tk.OPEN_ARROW): # Contaminated
            if self.expect_closing():
                return

            self.definition()


        raise SyntaxError('Object disclosed')


    def parse(self):
        while self._accept(Tk.OPEN_ARROW):
            self.definition()



args = sys.argv
if len(args) > 1:
    path = pathlib.Path(sys.argv[1])

    if path.is_file():
        with open(path, encoding="utf-8") as f:
            tokens = []
            Tokenizer().tokenize(tokens, f)
            print(tokens)
            token_iterator = TokenIterator(tokens)
            Parser(token_iterator).parse()
