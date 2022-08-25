class Word:
    def __init__(self, word: str):
        self.word = word.lower()

    def __iter__(self):
        return iter(self.word)

    def __next__(self):
        return next(self.word)

    def __str__(self):
        return self.word

    def solved(self, tips: set):
        return set(self.word) == tips

    def solvable(self, charset: str):
        return set(self.word).issubset(set(charset))

    def char_is_correct(self, char: str):
        return char in self.word