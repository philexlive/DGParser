import re
from enum import Enum
from wisayoparser import tokenname


class TokenizationError(Exception): pass


def check_id_or_key(s):
    """Check lexeme is the keyword or identifier

    :param s: str - input lexeme
    :return:
    """
    pattern = re.compile(r"^(true|false)$", re.IGNORECASE)
    if pattern.fullmatch(s):
        return tokenname.BoolLiteral(s)
    elif re.fullmatch(r"^[a-zA-Z].*$", s):
        return tokenname.Identifier(s)
    raise TokenizationError(f"Wrong lexeme {s}")


def check_number(s):
    if re.fullmatch(r"^[-+]?\d+$", s):
        return tokenname.NumberLiteral(s)
    elif re.fullmatch(r"^[-+]?(\d+|\d*\.\d+)$", s):
        return tokenname.FloatLiteral(s)
    raise SyntaxError(f"Unexpected literal {s}.")


def check_operator(s):
    return {
        '<': tokenname.OpenArrow(),
        '>': tokenname.CloseArrow(),
        '=': tokenname.Assign(),
        '/': tokenname.Slash(),
        '+': tokenname.Plus(),
        '-': tokenname.Minus()
    }[s]


def is_delimiter(s):
    return s in [' ', '\n', '\t', '<', '>', '=', '/', '', '-', '+']


def is_operator(s):
    return s in ['<', '>', '=', '/', '-', '+']


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


    def tokenize(self, file, stream):
        st = self.St
        
        state = st.INITIAL
        buffer = ''
        while state != st.FINISH:
            c = file.read(1)

            match state:
                case st.INITIAL:
                    if is_delimiter(c):
                        if is_operator(c):
                            stream.append(check_operator(c))
                    elif is_letter(c):
                        state = st.READING_ID_OR_KEY
                        buffer += c
                    elif is_digit(c) or is_dot(c):
                        state = st.READING_NUMBER
                        buffer += c
                    elif is_quote(c):
                        state = st.READING_STRING
                    else:
                        raise TokenizationError(f"{c, file.tell()}")

                case st.READING_ID_OR_KEY:
                    if is_delimiter(c):
                        stream.append(check_id_or_key(buffer))

                        if is_operator(c):
                            stream.append(check_operator(c))
                            
                        buffer = ''
                        state = st.INITIAL
                    else:
                        buffer += c
                
                case st.READING_NUMBER:
                    if is_delimiter(c):
                        stream.append(check_number(buffer))

                        if is_operator(c):
                            stream.append(check_operator(c))

                        buffer = ''
                        state = st.INITIAL
                    elif is_letter(c):
                        raise TokenizationError(f"Unexpected literal {buffer}.")
                    else:
                        buffer += c
                
                case st.READING_STRING:
                    if is_quote(c):
                        stream.append(tokenname.StringLiteral(buffer))
                        buffer = ''
                        state = st.INITIAL
                    else:
                        buffer += c
            if c == '':
                state = st.FINISH

        stream.reset()