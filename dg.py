from enum import Enum
import re
import sys
import pathlib


class Tk(Enum):
    OPEN_ARROW=0
    CLOSE_ARROW=1
    ASSIGN_OPERATOR=3
    SLASH_OPERATOR=4
    LITERAL=5
    IDENTIFIER=6



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
                        tokens.append((Tk.LITERAL, buffer))
                        buffer = ''
                        state = St.INITIAL
                    else:
                        buffer += c
            if c == '':
                state = St.FINISH


    def is_letter(self, s):
        if re.fullmatch(r"^[a-zA-Z]$", s):
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
            return Tk.LITERAL
        elif re.fullmatch(r"^[-+]?(\d+|\d*\.\d+)$", s):
            return Tk.LITERAL
            
        raise SyntaxError(f"Unexpected literal {s}.")

    def check_id_or_key(self, s):
        pattern = re.compile(r"^(true|false)$", re.IGNORECASE)
        if pattern.fullmatch(s):
            return Tk.LITERAL
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


class AttributeNode(Node):
    def __init__(self, name):
        self.name = name
        self.value = ''


class DefinitionNode(Node):
    def __init__(self):
        self.attributes = []
        self.nodes = []

class Parser:
    tree = DefinitionNode()

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


    def attribute(self, name):
        self._expect(Tk.ASSIGN_OPERATOR)
        node = AttributeNode(name)

        value = self.sym[1]
        if self._accept(Tk.LITERAL):
            node.value = value
            return node
        else:
            raise SyntaxError('Unexpected symbol or object disclosed')


    def definition(self):
        def expect_closing():
            if self._accept(Tk.SLASH_OPERATOR):
                self._expect(Tk.CLOSE_ARROW)
                return True
            return False

        self._expect(Tk.IDENTIFIER)

        node = DefinitionNode()

        # Attributes
        identifier = self.sym[1]
        while self._accept(Tk.IDENTIFIER):
            node.attributes.append(self.attribute(identifier))
            identifier = self.sym[1]
        del identifier

        if expect_closing():
            return node

        self._expect(Tk.CLOSE_ARROW)

        while self._accept(Tk.OPEN_ARROW): # Contaminated
            if expect_closing():
                return node

            node.nodes.append(self.definition())

        raise SyntaxError('Object disclosed')


    def parse(self, tree):
        while self._accept(Tk.OPEN_ARROW):
            tree.append(self.definition())



args = sys.argv
if len(args) > 1:
    path = pathlib.Path(sys.argv[1])

    if path.is_file():
        with open(path, encoding="utf-8") as f:
            tokens = []
            Tokenizer().tokenize(tokens, f)

            tree = []
            token_iterator = TokenIterator(tokens)
            Parser(token_iterator).parse(tree)
            del tokens
            print(tree)
