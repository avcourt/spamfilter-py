import unittest
import spamfilter as sf


class TestSpamfilter(unittest.TestCase):
    
    def test_tokens(self):
        test_str = 'abcdefg'
        toks = sf.tokens(test_str, tok_size=4)
        self.assertEqual(toks, ['abcd', 'bcde', 'cdef', 'defg'])

        toks = sf.tokens(test_str)
        self.assertEqual(toks, ['abc', 'bcd', 'cde', 'def', 'efg'])

