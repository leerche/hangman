
import csv
from pathlib import Path
import string
from data.decode import WordDecode
from factories.game_factory import GameFactory
from models.config import Config
from models.player import Player
from models.time_config import TimeConfig
from models.time_game import TimeGame
from models.word import Word

class GameController:
    def __init__(self) -> None:
        pass

    # Spielstart:
    # derzeit erlauben wir nur eine feste Anzahl an falsch geratenen Buchstaben
    def start(self, name: str, mode: str, minutes: int) -> None:
        word_decode = WordDecode()
        word_decode.read()
        #game_factory = GameFactory(Player(name), WordDecode().getWord(), string.ascii_lowercase + 'üöä', 6, mode, minutes)
        game_factory = GameFactory(Player(name), Word("t"), string.ascii_lowercase + 'üöä', 6, mode, minutes)
        
        self.game = game_factory.make_game()
        self.savePlayerNameToCSV(name);
        
    # Speichere den Spielernamen in der Datei names.csv:
    def savePlayerNameToCSV(self, player: str):
        with open ('names.csv', 'r') as name_fread:
            names_reader = csv.reader(name_fread)
            for row in names_reader:
                if row == [player]:
                    return
        with open('names.csv', 'a') as name_file:
            name_writer =  csv.writer(name_file, delimiter=',', quotechar='"')
            name_writer.writerow([player])

    # Einen Buchstaben erraten:
    # Wenn er richtig ist, wird der Buchstabe von der Methode zurück gegeben:
    def tip(self, tip: str) -> None:
        if not self.game.isValidTip(tip):
            return
        if self.game.isFinished():
            return
        self.game.tip(tip)
    
    # Das aktuelle Lösungswort ausgeben:
    # Erratene Buchstaben werden angezeigt und noch nicht erratene Buchstaben
    # werden durch einen Unterstrich repräsentiert.
    def word_status(self) -> str: 
        # TODO: word_status als Klasse mit einer toString-Methode implementieren
        return ''.join([char if char else ' _ ' for char in self.game.word_status()])

    # Den Spielernamen ausgeben
    def getName(self) -> str:
        return self.game.getPlayerName()

    # Gibt alle Zeichen aus, die bisher geraten wurden:
    # (in alphabetischer Reihenfolge)
    def tips(self) -> str:
        return ' '.join(sorted([char for char in self.game.unique_tips()]))

    # Gibt an, wie viele gültige (validierte) Tips bereits gemacht wurden:
    def tip_amount(self) -> str:
        return str(self.game.tip_amount())

    # Gibt an, wie viele korrekte Tips bereits gemacht wurden:
    def correct_tip_amount(self) -> str:
        return str(self.game.correct_tip_amount())

    # Autovervollständigung für die Eingabe der Spielernamen:
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

    # Routine bei gewonnenem Spiel:
    def isWon(self) -> bool:
        return self.game.isWon()
        
    # Routine bei verlorenem Spiel:
    def isLost(self) -> bool:
        return self.game.isLost()

    # Gibt an, ob es sich um ein Spiel auf Zeit handelt:
    def isTimeGame(self) -> bool:
        return isinstance(self.game, TimeGame)