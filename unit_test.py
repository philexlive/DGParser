from dg import LexicalAnalyzer
import unittest

class TestTokenizer(unittest.TestCase):
    _la = LexicalAnalyzer()
    def test_files(self):
        tk_control = []
        tk_test = []
        with open('res.phyobj', encoding="utf-8") as f:
            self._la.tokenize(tk_control, f)
        with open('rescp.phyobj', encoding="utf-8") as f:
            self._la.tokenize(tk_test, f)
        self.assertEqual(tk_control, tk_test)

unittest.main()
