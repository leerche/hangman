from Config import Config
from Word import Word
from Player import Player

class Game:
    def __init__(self, player: Player, word: Word, config: Config):
        self.config = config
        self.player = player
        self.char_dict = {}
        for char in config.charset:
            self.char_dict[char] = False
        self.word = word

    def tips(self) -> set: 
        return set({k:v for (k,v) in self.char_dict.items() if v}.keys())
        
    def correct_tips(self) -> set:
        return set([x for x in self.tips() if self.word.char_is_correct(x)])

    def missing_tips(self) -> set:
        return set([x for x in self.word if not self.char_dict[x]])
        
    def word_status(self) -> list:
        return list(map(lambda x: x if x in self.correct_tips() else False, self.word))
    
    def tip_amount(self) -> int:
        return len(self.tips())
    
    def wrong_tip_amount(self) -> int:
        return self.tip_amount() - len(self.correct_tips())

    def tip(self, char: str) -> None:
        self.char_dict[char] = True

