from models.config import Config

class TimeConfig(Config):
    def __init__(self, charset: str, wrong_tip_amount: int, seconds: int) -> None:
        self.seconds = seconds
        super().__init__(charset, wrong_tip_amount)
