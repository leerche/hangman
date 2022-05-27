from models.config import Config
from models.game import Game
from models.player import Player
from models.word import Word


class GameFactory:
    def __init__(self, player: Player, word: Word, config: Config) -> None:
        self.player = player
        self.word = word
        self.config = config

    def make_game(self) -> Game:
        if not self.word.solvable(self.config.charset):
            raise ValueError("The word is not solveable with the selected charset.")
        return Game(self.player, self.word, self.config)
