import numpy
from TextHandler import SentenceInfo


class StructureStatistic:
    def __init__(self, strcture: list):
        self.structure = strcture
        self.structure_quantity = 0
        self.morphologic_quantity = dict()
        self.morphologic_probability = dict()

    def addSentenceFeature(self, sentence_info: SentenceInfo):
        words = sentence_info.info
        self.structure_quantity += 1
        for word_index in range(len(words)):
            tag = words[word_index]['tag'][0]
            if self.morphologic_quantity.get(tag) is None:
                self.morphologic_quantity[tag] = numpy.zeros(len(self.structure))
                self.morphologic_quantity[tag][word_index] = 1
                self.morphologic_probability[tag] = numpy.zeros(len(self.structure))
                self.morphologic_probability[tag][word_index] = 1
            else:
                self.morphologic_quantity[tag][word_index] += 1
                self.morphologic_probability[tag][word_index] += 1

    def calculateProbability(self):
        for key, value in self.morphologic_probability.items():
            self.morphologic_probability[key] = value / self.structure_quantity

    def toDict(self) -> dict:
        return {'structure': self.structure, 'structure_quantity': self.structure_quantity, 'morphologic_quantity': {key: value.tolist() for key, value in self.morphologic_quantity.items()}, 'morphologic_probability': {key: value.tolist() for key, value in self.morphologic_probability.items()}}

    def toStructureStatistic(self, structure_statistic_dict: dict):
        self.structure = structure_statistic_dict['structure']
        self.structure_quantity = structure_statistic_dict['structure_quantity']
        self.morphologic_quantity = structure_statistic_dict['morphologic_quantity']
        self.morphologic_probability = structure_statistic_dict['morphologic_probability']

