import csv
import os
from models.config import Config
from models.word import Word
from models.player import Player


class Game(object):
    def __init__(self, player: Player, word: Word, config: Config):
        if not word.solvable(config.charset):
            raise ValueError(
                "The word is not solveable with the selected charset.")
        self.config = config
        self.player = player
        self.tips = list()
        self.word = word
        
    def unique_tips(self):
        return set(self.tips)

    def correct_tips(self) -> set:
        return set([x for x in self.unique_tips() if self.word.char_is_correct(x)])

    def wrong_tips(self) -> set:
        return set([x for x in self.unique_tips() if not self.word.char_is_correct(x)])

    def missing_tips(self) -> set:
        return set([x for x in self.word if x not in self.tips])

    def word_status(self) -> list:
        return list(map(lambda x: x if x in self.correct_tips() else False, self.word))

    def tip_amount(self) -> int:
        return len(self.tips)

    def isWon(self) -> bool:
        return self.word.solved(self.unique_tips())

    def isLost(self) -> bool:
        return self.wrong_tip_amount() > self.config.wrong_tip_amount

    def wrong_tip_amount(self) -> int:
        return len(self.wrong_tips())

    def correct_tip_amount(self) -> int:
        return len(self.correct_tips())

    
    def isFinished(self) -> bool:
        return self.isWon() or self.isLost()

    def isValidTip(self, char: str) -> bool:
        char = char.lower()
        if not char in self.config.charset:
            return False
        if not len(char):
            return False
        return True

    def tip(self, char: str) -> None:
        if self.isFinished():
            raise ValueError("The game is already finished")
        if not len(char):
            raise ValueError("No tip provided")
        char = char.lower()
        if not char in self.config.charset:
            raise ValueError("Character is not in charset")
        self.tips.append(char)