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
        return s in ['<','>','@','=','/']

    def is_delimiter(self, s):
        return s in [' ', '\n', '\t', '<', '>', '@', '=', '/', '']


    def check_operator(self, s):
        return {'<': Tk.OPEN_ARROW,
                '>': Tk.CLOSE_ARROW,
                '@': Tk.AT_OPERATOR,
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


class Parser:
    class St:
        INITIAL=0
        EXPECT_ATTR_OPENING=1
        EXPECT_ATTR_CLOSING=2
        EXPECT_BODY_CLOSING=3
        FINISH=12
        
    
    def parse(self, tokens, tree):
        St = self.St
        
        cursor = 0
        state = St.INITIAL
        opened_bodies=0

        buffer = '' # Just visualization purpose
        
        while state != St.FINISH:
            if cursor >= len(tokens):
                state = St.FINISH

            match state:
                case St.INITIAL:
                    if tokens[cursor][0] == Tk.OPEN_ARROW:
                        state = St.EXPECT_ATTR_OPENING

                        # Just visualization purpose
                        buffer += '\t'*opened_bodies
                        buffer += tokens[cursor][1]

                case St.EXPECT_ATTR_OPENING:
                    if tokens[cursor][0] == Tk.IDENTIFIER:
                        state = St.EXPECT_ATTR_CLOSING
                        opened_bodies += 1

                        # Just visualization purpose
                        buffer += tokens[cursor][1]
                        print(buffer, end=' ')
                        buffer = ''
                    elif tokens[cursor][0] == Tk.SLASH_OPERATOR:
                        state = St.EXPECT_BODY_CLOSING
                        
                        # Just visualization purpose
                        buffer += tokens[cursor][1]
                
                case St.EXPECT_ATTR_CLOSING:
                    if tokens[cursor][0] == Tk.SLASH_OPERATOR:
                        state = St.EXPECT_BODY_CLOSING

                        # Just visualization purpose
                        buffer += tokens[cursor][1]
                    elif tokens[cursor][0] == Tk.CLOSE_ARROW:
                        state = St.INITIAL

                        # Just visualization purpose
                        buffer += tokens[cursor][1]
                        print(buffer)
                        buffer = ''
                        print(("\t"*opened_bodies) + "This body could have children")
                case St.EXPECT_BODY_CLOSING:
                    if tokens[cursor][0] == Tk.CLOSE_ARROW:
                        state = St.INITIAL
                        opened_bodies -= 1

                        # Just visualization purpose
                        buffer += tokens[cursor][1]
                        if buffer.strip() == '</>':
                            print(("\t" * (opened_bodies)) + buffer.strip())
                        else:
                            print(buffer)
                        buffer = '' 

                    else:
                        raise SyntaxError("> was expected")
                        

            
            cursor += 1
        print(opened_bodies)


class LexicalAnalyzer:
    tokenize = Tokenizer().tokenize
    parse = Parser().parse

args = sys.argv
if len(args) > 1:
    path = pathlib.Path(sys.argv[1])

    if path.is_file():
        with open(path, encoding="utf-8") as f:
            tokens = []
            LexicalAnalyzer().tokenize(tokens, f)
            #for tk in tokens:
            #    print(tk)
            tree = {}
            LexicalAnalyzer().parse(tokens, tree)
            print(tree)
