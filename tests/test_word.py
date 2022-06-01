import unittest

from models.word import Word


class TestWordMethods(unittest.TestCase):
    def setUp(self):
        self.word = Word("Mega")
    
    def test_is_lower(self):
        self.assertEqual(self.word.word, "mega")

    def test_solvable(self):
        self.assertTrue(self.word.solvable("mega"))
        self.assertFalse(self.word.solvable("ega"))

    def test_char_is_correct(self):
        self.assertTrue(self.word.char_is_correct("m"))
        self.assertFalse(self.word.char_is_correct("x"))

    def test_solved(self):
        self.assertFalse(self.word.solved(set(["m"])))
        self.assertTrue(self.word.solved(set(["m", "e", "g", "a"])))
