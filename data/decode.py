from base64 import decode
import codecs
import csv
from random import randint
from models.word import Word
"""
Klasse zum Auslesen und Entschlüsseln der Lösungswörter:
"""

class WordDecode ():
    
    # Konstruktor:
    def __init__(self) -> None:
        self.Decodiert = []

    # Auslesen und entschlüsseln der Lösungswörter:
    def read(self):
        with open('data/words.csv') as csv_schreib_datei:
            CSVWords = csv.reader(csv_schreib_datei, delimiter=",")        
            for row in CSVWords:
                for word in row:
                    word = codecs.decode(word, 'rot_13')
                    self.Decodiert.append(word)

    # Methode für den Abruf eines zufällig ausgewählten Lösungswortes:
    def getWord(self):
        value = randint(0,len(self.Decodiert) - 1)
        return Word(self.Decodiert[value])

