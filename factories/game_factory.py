from data.decode import WordDecode
from models.config import Config
from models.game import Game
from models.player import Player
from models.time_game import TimeGame
from models.time_config import TimeConfig
"""
Erstellung eines neuen Spiels mittels Fabrikmethode (Pattern)
"""

class GameFactory:
    def __init__(self, player: Player, charset: str, wrong_tip_amount: int, mode: str, minutes: int) -> None:
        self.player = player
        self.wrong_tip_amount = wrong_tip_amount
        self.mode = mode
        self.charset = charset
        self.minutes = minutes

    def make_game(self) -> Game:
        if self.mode == "time":
            return TimeGame(self.player,  WordDecode().getWord(), TimeConfig(self.charset, self.wrong_tip_amount, self.minutes * 60))
        return Game(self.player, WordDecode().getWord(), Config(self.charset, self.wrong_tip_amount))
