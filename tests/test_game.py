import string
import unittest
from models.game import Game
from models.config import Config
from models.player import Player
from models.word import Word


class TestGameMethods(unittest.TestCase):
    def setUp(self):
        self.game = Game(Player("Lea"), Word("Hallo"), Config(string.ascii_lowercase, 8))

    def test_tips(self):
        self.assertSetEqual(self.game.tips, set())
        self.game.tip("s")
        self.game.tip("A")
        self.game.tip("s")
        self.assertSetEqual(self.game.tips, set(["s", "a"]))

    def test_tip_amount(self):
        self.assertEqual(0, self.game.tip_amount())
        self.game.tip("L")
        self.assertEqual(1, self.game.tip_amount())

    def test_word_status(self):
        self.assertListEqual(self.game.word_status(), [False, False, False, False, False])
        self.game.tip("l")
        self.assertListEqual(self.game.word_status(), [False, False, "l", "l", False])

    def test_correct_tips(self):
        correct_tips = set()
        self.assertSetEqual(self.game.correct_tips(), correct_tips)
        self.game.tip("h")
        correct_tips.add("h")
        self.assertSetEqual(self.game.correct_tips(), correct_tips)
        self.game.tip("l")
        correct_tips.add("l")
        self.assertSetEqual(self.game.correct_tips(), correct_tips)
        self.game.tip("s")
        self.assertSetEqual(self.game.correct_tips(), correct_tips)

    def test_wrong_tips(self):
        wrong_tips = set()
        self.assertSetEqual(self.game.wrong_tip(), wrong_tips)
        self.game.tip("p")
        wrong_tips.add("p")
        self.assertSetEqual(self.game.wrong_tip(), wrong_tips)
        self.game.tip("x")
        wrong_tips.add("x")
        self.assertSetEqual(self.game.wrong_tip(), wrong_tips)
        self.game.tip("l")
        self.assertSetEqual(self.game.wrong_tip(), wrong_tips)
    
    def test_missing_tips(self):
        missing_tips = set()
        missing_tips = set(["h", "a", "l", "o"])
        self.assertSetEqual(self.game.missing_tips(), missing_tips)
        self.game.tip("o")
        missing_tips.remove("o")
        self.assertSetEqual(self.game.missing_tips(), missing_tips)

    def test_invalid_char(self):
        with self.assertRaises(ValueError):
            self.game.tip("1")
