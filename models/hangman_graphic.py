import math
import re


class HangmanGraphic:

    GRAPHIC_POOL = ['''
\t+--------------+
\t   |\t|
\t\t|
\t\t|
\t\t|
\t\t|
=================''','''
\t+--------------+
\t   |\t|
\t  O\t|
\t\t|
\t\t|
\t\t|
=================''','''
\t+--------------+
\t   |\t|
\t  O\t|
\t   |\t|
\t\t|
\t\t|
=================''', '''
\t+--------------+
\t   |\t|
\t  O\t|
\t /|  \t|
\t\t|
\t\t|
=================''', '''
\t+--------------+
\t   |\t|
\t  O\t|
\t /|\ \t|
\t    \t|
\t\t|
=================''', '''
\t+--------------+
\t   |\t|
\t  O\t|
\t /|\ \t|
\t /   \t|
\t\t|
=================''', '''
\t+--------------+
\t   |\t|
\t  O\t|
\t /|\ \t|
\t / \ \t|
\t\t|
=================
''']
    GRAPHIC_INDEX: int

    def __init__(self):
        self.prepareGraphic()

    def prepareGraphic(self):
        self.GRAPHIC_INDEX = 0

    def updateGraphic(self):
      if self.GRAPHIC_INDEX < len(self.GRAPHIC_POOL)-1:
        self.GRAPHIC_INDEX += 1

    def getGraphic(self):
        return self.GRAPHIC_POOL[self.GRAPHIC_INDEX]