import re

from wisayoparser import tokenname as tk


class ParsingError(Exception): pass


class AttributeNode:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        print(f"Attribute{self.name, self.value}")


class DefinitionNode:
    def __init__(self, name):
        self.name = name
        self.attributes = []
        self.nodes = []

    def __repr__(self):
        attributes = '\n\t'.join([f"Attribute{attr.name, attr.value}" for attr in self.attributes])
        nodes = '\n\t'.join([f"DefinitionNode({node.name})" for node in self.nodes])
        return f"DefinitionNode({self.name})\n\t" + attributes + "\n\n\t" + nodes


class Parser:
    def __init__(self, stream):
        self._stream = stream
        self._sym = None
        self._next_sym()

    def _next_sym(self):
        try:
            self._sym = next(self._stream)
        except StopIteration:
            return

    def _accept(self, sym):
        if isinstance(self._sym, sym):
            self._next_sym()
            return True
        return False

    def _expect(self, sym):
        if self._accept(sym):
            return
        raise ParsingError('Unexpected symbol')


    def _attribute(self, name):
        self._expect(tk.Assign)

        value = self._sym.value
        if self._accept(tk.NumberLiteral):
            return AttributeNode(name, int(value))
        elif self._accept(tk.FloatLiteral):
            return AttributeNode(name, float(value))
        elif self._accept(tk.BoolLiteral):
            if re.match(r"^true$", value, re.IGNORECASE):
                return AttributeNode(name, True)
            elif re.match(r"^false$", value, re.IGNORECASE):
                return AttributeNode(name, False)
            raise ParsingError("Unexpected value instead of bool")
        elif self._accept(tk.StringLiteral):
            return AttributeNode(name, value)

        raise ParsingError('Unexpected symbol or object disclosed')


    def _definition(self):

        # Open definition
        def expect_closing():
            if self._accept(tk.Slash):
                self._expect(tk.CloseArrow)
                return True
            return False

        definition_name = self._sym.value

        self._expect(tk.Identifier)

        node = DefinitionNode(definition_name)
        del definition_name

        # Attributes
        identifier = self._sym.value
        while self._accept(tk.Identifier):
            node.attributes.append(self._attribute(identifier))
            identifier = self._sym.value
        del identifier

        # Closing definition
        if expect_closing():
            return node

        self._expect(tk.CloseArrow)

        # Sub objects
        while self._accept(tk.OpenArrow): # Contaminated
            if expect_closing():
                return node

            node.nodes.append(self._definition())

        raise ParsingError('Object disclosed')


    def parse(self):
        if self._stream.index >= len(self._stream.data):
            raise ParsingError('Empty data')

        self._expect(tk.OpenArrow)

        ast = self._definition()

        if self._stream.index < len(self._stream.data):
            self._stream.reset()
            raise ParsingError('Extra symbols were added after object implementation')
        self._stream.reset()

        return ast
