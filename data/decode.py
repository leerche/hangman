from base64 import decode
import codecs
import csv
from encodings import utf_8
from random import randint
from models.word import Word
Decodiert = []
i= 0;

class WordDecode ():
    
    def __init__(self) -> None:
        pass

    def read(self):
        with open('data/words.csv') as csv_schreib_datei:
            CSVWords = csv.reader(csv_schreib_datei, delimiter=",")        
            for row in CSVWords:
                for word in row:
                    word = codecs.decode(word, 'rot_13')
                    Decodiert.append(word)

    def getWord(self):
        value = randint(0,len(Decodiert) - 1)
        return Word(Decodiert[value])

