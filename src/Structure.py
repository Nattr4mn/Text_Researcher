import pymorphy2


class Structure:
    def __init__(self):
        self.__standart_structure = []
        self.__pos_structure = []
        self.__morphologic_structure = []
        self.count = 1
        self.frequency = 0

    @property
    def standart(self):
        return self.__standart_structure

    @property
    def pos(self):
        return self.__pos_structure

    @property
    def morphologic(self):
        return self.__morphologic_structure

    def createStructure(self, sentence_token: list):
        self.__clearStructures()
        morph = pymorphy2.MorphAnalyzer()
        for word_token in sentence_token:
            word_info = morph.parse(word_token)[0]
            word_characteristic = str.split(' '.join(str.split(str(word_info.tag), ',')), ' ')
            if word_characteristic[0] == 'PNCT':
                self.__standart_structure.append(str(word_info.word))
                self.__pos_structure.append(str(word_info.word))
                self.__morphologic_structure.append(str(word_info.word))
            else:
                self.__standart_structure.append('WORD')
                self.__pos_structure.append(word_characteristic[0])
                self.__morphologic_structure.append(str(word_info.tag))

    def toList(self) -> list:
        return [self.__standart_structure, self.__pos_structure, self.__morphologic_structure, self.count]

    @staticmethod
    def toStructures(data: list):
        structure = Structure()
        structure.__constructor(data[0], data[1], data[2], data[3])
        return structure

    def __constructor(self, standart_structure: list, pos_structure: list, morphologic_structure: list, count: int):
        self.__standart_structure = standart_structure
        self.__pos_structure = pos_structure
        self.__morphologic_structure = morphologic_structure
        self.count = count

    def __clearStructures(self):
        self.__standart_structure.clear()
        self.__pos_structure.clear()
        self.__morphologic_structure.clear()