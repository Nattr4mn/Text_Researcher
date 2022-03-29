import pymorphy2
import re


class Word:
    def __init__(self, word: str):
        self.__word = word
        self.__characteristic = []
        self.count = 1
        self.frequency = 0

    @property
    def word(self):
        return self.__word

    @property
    def caracteristic(self):
        return self.__characteristic

    @staticmethod
    def toWord(data: list):
        word = Word(data[0])
        word.__constructor(data[1], int(data[2]), float(data[3]))
        return word

    def toList(self):
        return [self.word, self.characteristic, self.count, self.frequency]

    def exploreWord(self):
        morph = pymorphy2.MorphAnalyzer()
        word_info = morph.parse(self.word)[0]
        self.characteristic = str.split(' '.join(str.split(str(word_info.tag), ',')), ' ')

    def __constructor(self, characteristic: list, count: int, frequency: float):
        self.characteristic = characteristic
        self.count = count
        self.frequency = frequency
