from enum import Enum
import re


class Tk(Enum):
    OPEN_ARROW=0
    CLOSE_ARROW=1
    ASSIGN_OPERATOR=3
    SLASH_OPERATOR=4
    NUMBER_LITERAL=5
    FLOAT_LITERAL=6
    BOOL_LITERAL=7
    STR_LITERAL=8
    IDENTIFIER=9

def check_id_or_key(s):
    pattern = re.compile(r"^(true|false)$", re.IGNORECASE)
    if pattern.fullmatch(s):
        return Tk.BOOL_LITERAL
    return Tk.IDENTIFIER

def check_number(s):
    if re.fullmatch(r"^[-+]?\d+$", s):
        return Tk.NUMBER_LITERAL
    elif re.fullmatch(r"^[-+]?(\d+|\d*\.\d+)$", s):
        return Tk.FLOAT_LITERAL

    raise SyntaxError(f"Unexpected literal {s}.")

def check_operator(s):
    return {'<': Tk.OPEN_ARROW,
            '>': Tk.CLOSE_ARROW,
            '=': Tk.ASSIGN_OPERATOR,
            '/': Tk.SLASH_OPERATOR}[s]

def is_delimiter(s):
    return s in [' ', '\n', '\t', '<', '>', '=', '/', '']

def is_operator(s):
    return s in ['<', '>', '=', '/']

def is_quote(s):
    return s == '"'

def is_dot(s):
    return s == '.'

def is_digit(s):
    if re.fullmatch(r"^\d$", s):
        return True
    return False

def is_letter(s):
    if re.fullmatch(r"^[a-zA-Z]$", s):
        return True
    return False


class Tokenizer:
    class St(Enum):
        INITIAL=0
        FINISH=1
        READING_ID_OR_KEY=2
        READING_NUMBER=3
        READING_STRING=4

    def tokenize(self, tokens, file):
        st = self.St
        
        state = st.INITIAL
        buffer = ''
        while state != st.FINISH:
            c = file.read(1)

            match state:
                case st.INITIAL:
                    if is_delimiter(c):
                        if is_operator(c):
                            tokens.append((check_operator(c), c))
                    elif is_letter(c):
                        buffer += c
                        state = st.READING_ID_OR_KEY
                    elif is_digit(c) or is_dot(c):
                        buffer += c
                        state = st.READING_NUMBER
                    elif is_quote(c):
                        state = st.READING_STRING

                case st.READING_ID_OR_KEY:
                    if is_delimiter(c):
                        tokens.append((check_id_or_key(buffer), buffer))

                        if is_operator(c):
                            tokens.append((check_operator(c), c))
                            
                        buffer = ''
                        state = st.INITIAL
                    else:
                        buffer += c
                
                case st.READING_NUMBER:
                    if is_delimiter(c):
                        tokens.append((check_number(buffer), buffer))

                        if is_operator(c):
                            tokens.append((check_operator(c), c))

                        buffer = ''
                        state = st.INITIAL
                    elif is_letter(c):
                        raise SyntaxError(f"Unexpected literal {buffer}.")
                    else:
                        buffer += c
                
                case st.READING_STRING:
                    if is_quote(c):
                        tokens.append((Tk.STR_LITERAL, buffer))
                        buffer = ''
                        state = st.INITIAL
                    else:
                        buffer += c
            if c == '':
                state = st.FINISH


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


class ValType(Enum):
    INT='int'
    FLOAT='float'
    BOOL='bool'
    STR='str'

class Node:
    pass


class AttributeNode(Node):
    def __init__(self, name):
        self.name = name
        self.value = ''
        self.val_type = None


class DefinitionNode(Node):
    def __init__(self):
        self.attributes = []
        self.nodes = []


class Parser:
    tree = DefinitionNode()

    def __init__(self, tki):
        self._tki = tki
        self._sym = ''
        self._next_sym()

    def _next_sym(self):
        try:
            self._sym = next(self._tki)
        except StopIteration:
            return

    def _accept(self, sym):
        if self._sym[0] == sym:
            self._next_sym()
            return True
        return False

    def _expect(self, sym):
        if self._accept(sym):
            return
        raise SyntaxError('Unexpected symbol')


    def _attribute(self, name):
        self._expect(Tk.ASSIGN_OPERATOR)
        node = AttributeNode(name)

        value = self._sym[1]
        if self._accept(Tk.NUMBER_LITERAL):
            node.value = value
            node.val_type = ValType.INT
            return node
        if self._accept(Tk.FLOAT_LITERAL):
            node.value = value
            node.val_type = ValType.FLOAT
            return node
        if self._accept(Tk.BOOL_LITERAL):
            node.value = value
            node.val_type = ValType.BOOL
            return node
        if self._accept(Tk.STR_LITERAL):
            node.value = value
            node.val_type = ValType.STR
            return node
        else:
            raise SyntaxError('Unexpected symbol or object disclosed')


    def _definition(self):
        def expect_closing():
            if self._accept(Tk.SLASH_OPERATOR):
                self._expect(Tk.CLOSE_ARROW)
                return True
            return False

        self._expect(Tk.IDENTIFIER)

        node = DefinitionNode()

        # Attributes
        identifier = self._sym[1]
        while self._accept(Tk.IDENTIFIER):
            node.attributes.append(self._attribute(identifier))
            identifier = self._sym[1]
        del identifier

        if expect_closing():
            return node

        self._expect(Tk.CLOSE_ARROW)

        while self._accept(Tk.OPEN_ARROW): # Contaminated
            if expect_closing():
                return node

            node.nodes.append(self._definition())

        raise SyntaxError('Object disclosed')

    def parse(self, tree):
        while self._accept(Tk.OPEN_ARROW):
            tree.append(self._definition())
