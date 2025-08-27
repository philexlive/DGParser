# About

A parser for custom domain-specific language.

First of all, the parser is made for the [Wisayo Engine](https://github.com/philexlive/WisayoEngine), I recommend you check it out.

This parser has three main classes which will be used in your code:

- `Tokenizer`: Handles tokenization of any row file.
- `Stream`: Iterable class containing tokens
- `Parser`: Handles parsing from Tokens instance

## Quick start

**Install dependencies:**

```bash
pip install git+https://github.com/philexlive/WisayoParser.git
```

**Script file:**

```python
from wisayoparser import Tokenizer, Parser, TokensStream

with open('player.txt') as f:
    tokenizer = Tokenizer()

    stream = TokensStream()
    tokenizer.tokenize(f, stream)

    ast = Parser(stream).parse()
```

**Object to be parsed:**

```
<GameObject
    name="Player"
    x=87.2
    y=2.0 >

    <GameObject name="RightHand" />

    <Sprite>
        <Texture resource="res/some_texture.texture" />
    </>
</>
```
