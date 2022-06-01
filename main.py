import string
from time import sleep
from factories.game_factory import GameFactory
from models.game import Game
from models.player import Player
from models.time_config import TimeConfig
from models.word import Word
from models.config import Config

#game_factory = GameFactory(Player("Lea"), Word("Hallo"), Config(string.ascii_lowercase, 7))
game_factory = GameFactory(Player("Lea"), Word("Hallo"), TimeConfig(string.ascii_lowercase, 7, 2))

game = game_factory.make_game()
game.tip("a")
game.tip("b")
game.tip("y")
tips = game.tips
correct_tips = game.correct_tips()
missing_tips = game.missing_tips()
word_status = game.word_status()
tip_amount = game.tip_amount()
wrong_tip_amount = game.wrong_tip_amount()

prevlost = game.isLost()
sleep(2)
lost = game.isLost()

l = "s"
