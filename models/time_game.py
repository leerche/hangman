from datetime import datetime, timedelta
from models.time_config import TimeConfig
from models.word import Word
from models.player import Player
from models.game import Game

class TimeGame(Game):
    def __init__(self, player: Player, word: Word, config: TimeConfig):
        self.startTime = datetime.now()
        super().__init__(player, word, config)
        self.config = config

    def isLost(self) -> bool:
        return super().isLost() or self.startTime + timedelta(seconds=self.config.seconds) < datetime.now()

    

