import pathlib
import sys
from dgparser import *

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

            print(tree.nodes[3].nodes[0].attributes[1].val_type)
            print(tree.nodes[3].nodes[0].attributes[1].value)