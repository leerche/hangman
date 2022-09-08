
import csv
from pathlib import Path
import string
from data.decode import WordDecode
from factories import game_factory
from factories.game_factory import GameFactory
from models import hangman_graphic
from models.config import Config
from models.player import Player
from models.time_config import TimeConfig
from models.time_game import TimeGame
from models.word import Word
from models.hangman_graphic import HangmanGraphic

class GameController:
    def __init__(self) -> None:
        pass

    # currently we allow a fixed amount of allowed wrong tips.
    # future: catch if you can actually fail with the wrong tip amount
    def start(self, name: str, mode: str, minutes: int) -> None:
        word_decode = WordDecode()
        word_decode.read()
        #game_factory = GameFactory(Player(name), WordDecode().getWord(), string.ascii_lowercase + 'üöä', 6, mode, minutes)
        game_factory = GameFactory(Player(name), Word("testasd"), string.ascii_lowercase + 'üöä', 6, mode, minutes)
        
        self.game = game_factory.make_game()
        self.savePlayerNameToCSV(name)
        self.graphic = self.game.getGraphic()

    
    def savePlayerNameToCSV(self, player: str):
        with open ('names.csv', 'r') as name_fread:
            names_reader = csv.reader(name_fread)
            for row in names_reader:
                if row == [player]:
                    return
        with open('names.csv', 'a') as name_file:
            name_writer =  csv.writer(name_file, delimiter=',', quotechar='"')
            name_writer.writerow([player])

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
        return ' '.join(sorted([char for char in self.game.unique_tips()]))

    def tip_amount(self) -> str:
        return str(self.game.tip_amount())

    def correct_tip_amount(self) -> str:
        return str(self.game.correct_tip_amount())

    def get_names(self) -> list:
        names = []
        file = Path('names.csv')
        mode = 'r'
        if not file.is_file():
             mode ='w+'
            
        with open ('names.csv', mode) as name_fread:
            names_reader = csv.reader(name_fread)
            for row in names_reader:
                names += row
            name_fread.close()
        return names

    def isWon(self) -> bool:
        return self.game.isWon()

    def isLost(self) -> bool:
        return self.game.isLost()

    def isTimeGame(self) -> bool:
        return isinstance(self.game, TimeGame)