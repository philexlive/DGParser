# About

A parser for custom domain specific language.

Primarily, the parser is made for [Wisayo Engine](https://github.com/philexlive/WisayoEngine), I recommend to get acquainted with.

# How to use

This parser hase three main classes being used in your pipeline:

- `Tokenizer`: Handles tokenization of any row file.
- `Tokens`: Iterable class containing tokens
- `Parser`: Handles parsing from Tokens instance

## Sample

Code example:

```python
from wisayo.parser import Tokenizer, Parser

with open('res.phyobj') as f:
    try:
        # Tokenization
        tokens = Tokenizer().tokenize(f)
        
        print(tokens)

        # Parsing
        ast = Parser(tokens).parse()
        
        print(ast)
        print(ast.nodes[0].attributes[0].value)
    except SyntaxError as e:
        print(f"Error: {e}")
```

Your object to parse:

```
<PhyObj
    name="Player"
    x=87.234
    y=2.0 >

    <PhyObj
        name="RightHand"
    />
</>
```

# TODOs
- [x] Add tokenizer
- [x] Add parser
- [x] Add error handling
- [ ] Write docs
