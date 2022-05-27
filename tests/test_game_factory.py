import string
import unittest
from factories.game_factory import GameFactory
from models.config import Config
from models.player import Player

from models.word import Word


class TestGameFactoryMethods(unittest.TestCase):
    def test_solvable_error(self):
        factory = GameFactory(Player("Lea"), Word("1"), Config(string.ascii_lowercase, 8))
        with self.assertRaises(ValueError):
            factory.make_game()