from models.config import Config
from models.word import Word
from models.player import Player

class Game(object):
    # Konstruktor:
    def __init__(self, player: Player, word: Word, config: Config):
        # Prüfe, ob das Wort mit dem erlaubten Zeichensatz lösbar ist:
        if not word.solvable(config.charset):
            raise ValueError("The word is not solveable with the selected charset.")
        self.config = config
        self.player = player
        self.tips = list()
        self.word = word

    #
    def unique_tips(self):
        return set(self.tips)
    
    # Rückgabe einer unsortierten Liste mit den Buchstaben, die bereits erraten wurden:
    def correct_tips(self) -> set:
        return set([x for x in self.unique_tips() if self.word.char_is_correct(x)])

    # Rückgabe einer unsortierten Liste mit den Buchstaben, die falsch erraten wurden:
    def wrong_tips(self) -> set:
        return set([x for x in self.unique_tips() if not self.word.char_is_correct(x)])

    # Rückgabe einer unsortierten Liste mit den Buchstaben, die noch nicht erraten wurden:
    def missing_tips(self) -> set:
        return set([x for x in self.word if x not in self.tips])
        
    # Rückgabe einer Liste, mit allen bereits erratenen Buchstaben, nicht erratene Buchstaben sind false (bool):
    def word_status(self) -> list:
        return list(map(lambda x: x if x in self.correct_tips() else False, self.word))

    # Rückgabe der Anzahl aller bisher abgegebenen Tips:
    def tip_amount(self) -> int:
        return len(self.unique_tips())

    # Prüft, ob das Spiel gewonnen wurde:
    def isWon(self) -> bool:
        # true, wenn die erlaubte Anzahl an Tips nicht überschritten wurde:
        return self.word.solved(self.unique_tips())

    # Prüft, ob das Spiel verloren wurde:
    def isLost(self) -> bool:
        # true, wenn die erlaubte Anzahl falscher Tips überschritten wurde:
        return self.wrong_tip_amount() > self.config.wrong_tip_amount
    
    # Rückgabe der Anzahl bisher falsch erratener Buchstaben:
    def wrong_tip_amount(self) -> int:
        return len(self.wrong_tips())

    # Rückgabe der Anzahl bisher korrekt erratener Buchstaben:
    def correct_tip_amount(self) -> int:
        return len(self.correct_tips())
    
    # liefert true zurück, falls das Spiel bereits gewonnen oder veloren wurde:
    def isFinished(self) -> bool:
        return self.isWon() or self.isLost()

    # liefert true zurück, wenn der eingegebene Tip zulässig ist:
    def isValidTip(self, char: str) -> bool:
        char = char.lower()
        if not char in self.config.charset:
            return False
        if not len(char):
            return False
        return True

    # verarbeitet die Eingabe beim Erraten eines Buchstabens:
    def tip(self, char: str) -> None:
        # ist das Spiel bereits beendet worden?
        if self.isFinished():
            raise ValueError("The game is already finished")
        # wurde überhaupt etwas eingegeben?
        if not len(char):
            raise ValueError("No tip provided")
        # groß geschriebene Buchstaben verarbeiten:
        char = char.lower()
        # befindet sich der Buchstabe im erlaubten Zeichensatz?
        if not char in self.config.charset:
            raise ValueError("Character is not in charset")
        # verarbeite den zu erratenden Buchstaben:
        self.tips.append(char)

