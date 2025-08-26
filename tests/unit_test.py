import unittest
from src.wisayoparser.parser import Parser, Tokenizer, Tokens


class TestTokenizer(unittest.TestCase):

    def test_gives_ast(self):
        ast = None
        with open('tests/res.phyobj') as f:
            try:
                # Tokenization
                tokens = Tokenizer().tokenize(f)

                ast = Parser(tokens).parse()
            except SyntaxError as e:
                print(f"Error: {e}")

        expected = 'RightHand'
        actual = ast.nodes[0].attributes[0].value
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()