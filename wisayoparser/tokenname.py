from abc import ABC


class Token(ABC):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        if self.value:
            return f"{self.__class__.__name__}({self.value!r})"
        return f"{self.__class__.__name__}"


class OpenArrow(Token):
    def __init__(self):
        super().__init__(None)


class CloseArrow(Token):
    def __init__(self):
        super().__init__(None)


class AssignOperator(Token):
    def __init__(self):
        super().__init__(None)


class SlashOperator(Token):
    def __init__(self):
        super().__init__(None)


class Identifier(Token): pass


class NumberLiteral(Token): pass


class FloatLiteral(Token): pass


class BoolLiteral(Token): pass


class StringLiteral(Token): pass