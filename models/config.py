"""
Klasse zur Konfiguration eines Spiels.
Übergabe von:
  - erlaubter Zeichensatz
  - maximale Anzahl falscher Tips
"""
class Config(object):
    def __init__(self, charset: str, wrong_tip_amount: int) -> None:
        self.charset = charset
        self.wrong_tip_amount = wrong_tip_amount
