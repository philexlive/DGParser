# About

A parser for custom domain-specific language.

First of all, the parser is made for the [Wisayo Engine](https://github.com/philexlive/WisayoEngine), I recommend you check it out.

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

# Pipeline

There are several basic classes involved in the parsing process, these are `Tokenizer`, `TokensStream`, and `Parser`.

`Tokenizer` handles tokenization of any row file. It have a method `parse` which takes a **file** and **tokens stream** and handles reading the file and assigning appropriate tokens to your the **tokens stream**.

Tokenizer have some types of literal tokens represent numbers, strings and booleans. Already on tokenization process literal type definition happens. There could be `NumberLiteral` that is just integer, `FloatLiteral` represents float, `BoolLiteral` is **true|false**, and `StringLiteral` just a raw string.

Then `Parser` on initialization takes a **tokens stream**. then `parse` method used to make an AST from given **tokens stream**. It also processes convertion the type of **literal** to `int`,  `float`, `bool`, and `str`.

# Abstract Syntax Tree (AST)

The AST nodes represent two implementations `DefinitionNode` and `AttributeNode`.

**Definition** node an implementation consisting of such fields:

- `name`: Dependening on your interpreter, it could represent a type of the object or its unique name
- `attributes`: represents multiple of fields of an object
- `nodes`: Represents its child-parent relation, there could be its children **definition** nodes

**Attributes**:
- `name`: Represents field name of the **definition** it's in.
- `value`: Contains one primitve to be assigned to that field.

It will look something like this:
```
DefinitionNode('GameObject')
    AttributeNode('name', 'Player')
    AttributeNode('x', 87.2)
    AttributeNode('y', 2.0)

    DefinitionNode('GameObject')
    DefinitionNode('Sprite')
        ...
    ...
```

...
``
