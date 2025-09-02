import unittest
from wisayoparser import Tokenizer, Parser, TokensStream
from wisayoparser.tokenizer import TokenizationError
from wisayoparser.tokenname import OpenArrow, Identifier


class TestTokenizer(unittest.TestCase):
    tokenizer = Tokenizer()

    def test_gives_ast(self):
        ast = None
        with open('tests/res.txt') as f:
            # Tokenization

            stream = TokensStream()
            self.tokenizer.tokenize(f, stream)

            ast = Parser(stream).parse()

        self.assertEqual('RightHand', ast.nodes[0].attributes[0].value)
        self.assertEqual('Texture', ast.nodes[1].nodes[0].name)
        self.assertEqual(2.0, ast.attributes[2].value)


    def test_tokens(self):
        with open('tests/res.txt') as f:
            stream = TokensStream()
            self.tokenizer.tokenize(f, stream)
            self.assertIsInstance(next(stream), OpenArrow)
            self.assertIsInstance(next(stream), Identifier)

    def test_token_error(self):
        with open('tests/res_corrupted.txt') as f:
            stream = TokensStream()

            self.assertRaises(TokenizationError, self.tokenizer.tokenize, *[f, stream])


if __name__ == '__main__':
    unittest.main()
