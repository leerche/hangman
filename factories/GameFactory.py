from Game import Game
from Player import Player
from Word import Word
from Config import Config


class GameFactory:
    def __init__(self, player: Player, word: Word, config: Config) -> None:
        self.player = player
        self.word = word
        self.config = config

    def make_game(self) -> Game:
        if not self.word.solvable(self.config.charset):
            raise ValueError("The word is not solveable with the selected charset.")
        return Game(self.player, self.word, self.config)
