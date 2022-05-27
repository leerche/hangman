import string
from factories.game_factory import GameFactory
from models.game import Game
from models.player import Player
from models.word import Word
from models.config import Config


game_factory = GameFactory(Player("Lea"), Word("Hallo"), Config(string.ascii_lowercase, 7))

game = game_factory.make_game()
game = Game(Player("Lea"), Word("Hallo"), Config(string.ascii_lowercase, 7))
game.tip("a")
game.tip("b")
game.tip("y")
tips = game.tips
correct_tips = game.correct_tips()
missing_tips = game.missing_tips()
word_status = game.word_status()
tip_amount = game.tip_amount()
wrong_tip_amount = game.wrong_tip_amount()
l = "s"
