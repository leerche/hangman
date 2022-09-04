
import csv
import string
from data.decode import WordDecode
from factories.game_factory import GameFactory
from models.config import Config
from models.player import Player
from models.time_config import TimeConfig
from models.word import Word

class GameController:
    def __init__(self) -> None:
        pass

    # currently we allow a fixed amount of allowed wrong tips.
    # future: catch if you can actually fail with the wrong tip amount
    def start(self, name: str, mode: str, minutes: int) -> None:
        word_decode = WordDecode()
        word_decode.read()
        if(mode == "time"):
            game_factory = GameFactory(Player(name), WordDecode().getWord(), TimeConfig(string.ascii_lowercase + 'üöä', 6, minutes * 60))
        else:
            game_factory = GameFactory(Player(name), WordDecode().getWord(), Config(string.ascii_lowercase + 'üöä', 6))

        self.game = game_factory.make_game()
        self.savePlayerNameToCSV(name);
        
    
    def savePlayerNameToCSV(self, player: str):
        with open ('names.csv') as name_fread:
            names_reader = csv.reader(name_fread)
            for row in names_reader:
                if row == [player]:
                    return
        with open('names.csv', mode='a') as name_file:
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
        return ''.join([char for char in self.game.unique_tips()])

    def tip_amount(self) -> str:
        return str(self.game.tip_amount())

    def correct_tip_amount(self) -> str:
        return str(self.game.correct_tip_amount())

    def get_names(self) -> list:
        names = []
        with open ('names.csv') as name_fread:
            names_reader = csv.reader(name_fread)
            for row in names_reader:
                names += row
        return names

    def isWon(self) -> bool:
        return self.game.isWon()

    def isLost(self) -> bool:
        return self.game.isLost()