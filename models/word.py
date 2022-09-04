class Word:
    # Konstruktor:
    def __init__(self, word: str):
        self.word = word.lower()

    # magische Methode für Iterationen über das Lösungswort:
    def __iter__(self):
        return iter(self.word)

    # magische Methode, welche die Buchstaben des Lösungswort nacheinander ausgibt:
    def __next__(self):
        return next(self.word)

    # magische Methode, die das Lösungswort als String zurück gibt:
    def __str__(self):
        return self.word

    # liefert true zurück, wenn das Wort vollständig gelöst wurde:
    def solved(self, tips: set):
        return set(self.word) == tips

    # liefert true zurück, wenn das Wort mit dem erlaubten Zeichensatz lösbar ist:
    def solvable(self, charset: str):
        return set(self.word).issubset(set(charset))

    # liefert true zurück, wenn der Buchstabe korrekt ist:
    def char_is_correct(self, char: str):
        return char in self.word