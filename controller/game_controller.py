
import string
from factories.game_factory import GameFactory
from models.config import Config
from models.player import Player
from models.word import Word

class GameController:
    def __init__(self) -> None:
        pass

    def start(self, name: str, mode: str, minutes: int) -> None:
        game_factory = GameFactory(Player(name), Word("test"), Config(string.ascii_lowercase, 6))
        self.game = game_factory.make_game()

    def tip(self, tip: str) -> None:
        if not self.game.isValidTip(tip):
            return
        if self.game.isFinished():
            return
        self.game.tip(tip)

    def word_status(self) -> str: 
        # todo word status class with to string method
        return ''.join([char if char else ' _ ' for char in self.game.word_status()])

    def tips(self) -> str:
        return ''.join([char for char in self.game.unique_tips()])

    def tip_amount(self) -> str:
        return str(self.game.tip_amount())

    def correct_tip_amount(self) -> str:
        return str(self.game.correct_tip_amount())

    def get_names(self) -> list:
        return ["Lea", "Robert", "Christopher", "Jonas"]

    def isWon(self) -> bool:
        return self.game.isWon()

    def isLost(self) -> bool:
        return self.game.isLost()