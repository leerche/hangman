import string
from Config import Config
from Player import Player
from Word import Word
from factories.GameFactory import GameFactory


game_factory = GameFactory(Player("Lea"), Word("Hallo"), Config(string.ascii_lowercase, 7))

game = game_factory.make_game()
game.tip("a")
game.tip("b")
game.tip("y")
tips = game.tips()
correct_tips = game.correct_tips()
missing_tips = game.missing_tips()
word_status = game.word_status()
tip_amount = game.tip_amount()
wrong_tip_amount = game.wrong_tip_amount()
l = "s"
