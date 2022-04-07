from pymorphy2.analyzer import Parse


class Word:
    def __init__(self):
        self.__word = str
        self.__characteristic = []
        self.count = 1
        self.frequency = 0

    @property
    def word(self):
        return self.__word

    def parse(self, word_info: Parse):
        self.__word = word_info.word
        self.__characteristic = str.split(' '.join(str.split(str(word_info.tag), ',')), ' ')

    @property
    def characteristic(self):
        return self.__characteristic

    @staticmethod
    def toWord(data: list):
        word = Word()
        word.__constructor(data[0], data[1], int(data[2]), float(data[3]))
        return word

    def toList(self):
        return [self.word, self.characteristic, self.count, self.frequency]

    def __constructor(self, word: str, characteristic: list, count: int, frequency: float):
        self.__word = word
        self.__characteristic = characteristic
        self.count = count
        self.frequency = frequency
