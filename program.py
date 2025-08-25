import pathlib
import sys
from dgparser import *


class Tree:
    def __init__(self):
        self.name = ''
        self.x = 0.0
        self.y = 0.0
        self.children = None

class PhyObj(Tree):
    def __init__(self):
        super().__init__()
        self.inherit = False

class Text(Tree):
    def __init__(self):
        super().__init__()
        self.text = ''
        self.offset = 0


def visit(node):
    match node.definition_type:
        case 'PhyObj':
            o = PhyObj()
            set_attrs(o, node)
            set_children(o, node)
            return o
        case 'Text':
            o = Text()
            set_attrs(o, node)
            set_children(o, node)
            return o
        case _:
            raise TypeError('There is no such object type')


def set_attrs(obj, node):
    for attr in node.attributes:
        value = None
        match attr.val_type:
            case ValType.FLOAT:
                value = float(attr.value)
            case ValType.INT:
                value = int(attr.value)
            case ValType.BOOL:
                value = bool(attr.value)
            case ValType.STR:
                value = str(attr.value)

        if hasattr(obj, attr.name):
            obj_attr_type = type(getattr(obj, attr.name))
            if obj_attr_type == type(value):
                setattr(obj, attr.name, value)
            else:
                raise TypeError(f"Wrong type for {attr.name} "
                                f"expected {obj_attr_type}, "
                                f"got {type(value)}")
        else:
            raise NameError('No such attribute name')

def set_children(obj, node):
    if node.nodes:
        obj.children = []
        for sub in node.nodes:
            obj.children.append(visit(sub))

args = sys.argv
if len(args) > 1:
    path = pathlib.Path(sys.argv[1])

    if path.is_file():
        with open(path, encoding="utf-8") as f:
            tokens = []
            Tokenizer().tokenize(tokens, f)

            token_iterator = TokenIterator(tokens)
            tree = Parser(token_iterator).parse()
            del tokens
            print(tree)

            print(tree.nodes[4].nodes[0].attributes[1].val_type)
            print(tree.nodes[4].nodes[0].attributes[1].value)
            print(tree.nodes[4].nodes[0].definition_type)
            print(tree.nodes[2].attributes[0].value)

            root = visit(tree)
            print(root.children[2].text)
            print(root.children[2].offset)
            label = root.children[2]

            def draw_text(t):
                return " " * t.offset + t.text
            print(draw_text(label))