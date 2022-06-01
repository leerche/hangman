from models.config import Config
from models.game import Game
from models.player import Player
from models.time_game import TimeGame
from models.word import Word
from models.time_config import TimeConfig


class GameFactory:
    def __init__(self, player: Player, word: Word, config: Config) -> None:
        self.player = player
        self.word = word
        self.config = config

    def make_game(self) -> Game:
        if isinstance(self.config, TimeConfig):
            return TimeGame(self.player, self.word, self.config)
        return Game(self.player, self.word, self.config)
