import codecs
import csv
from encodings import utf_8
"""
In dieser Klasse werden die Lösungswörter werden verschlüsselt und in die Datei data/words.csv gespeichert.
"""
class WordEncode ():
    
    def __init__(self) -> None:
        pass

    def write(self):
        Woerter = [
            "Compiler",
            "Python",
            "Typ",
            "Recycling",
            "Paragraph",
            "Quelltext",
            "Schleifmaschine",
            "Steuerhinterziehung", 
            "Karpador", 
            "Atomkraftwerk",
            "Telekommunikationsgesetz",
            "Funktion",
            "Bredouille",
            "Chipsatz",
            "Microcontroller",
            "Übergabe",
            "Phasen",
            "Parabol",
            "Quinoa",
            "Quarantäne"
            ]
        Codiert = []
        i= 0
        with open('data/words.csv', 'w', encoding='utf_8') as csv_schreib_datei:
            writer = csv.writer(csv_schreib_datei, delimiter=",")        
            for wort in Woerter:
                wort = codecs.encode(wort, 'rot_13')
                Codiert.insert(i+1,wort)
            
            writer.writerow(Codiert)

