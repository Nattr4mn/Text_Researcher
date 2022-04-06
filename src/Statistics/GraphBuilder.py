import numpy as np


class GraphBuilder:
    def __init__(self):
        self.__graph = None
        self.__graphSize = 0

    @property
    def graph(self):
        return self.__graph

    def createGraph(self, pos_structure: list):
        dictionary = self.__createDictionary(pos_structure)
        self.__graph = np.zeros((self.__graphSize, self.__graphSize))
        for sentence in pos_structure:
            for word in sentence:
                for other_words in sentence:
                    if other_words != word:
                        self.__graph[dictionary[word]][dictionary[other_words]] += 1
        return self.__graph

    def __createDictionary(self, tokens):
        dictionary = {}
        for sentence in tokens:
            for word in sentence:
                if dictionary.get(word) is None:
                    dictionary.update({word: self.__graphSize})
                    self.__graphSize += 1
        return dictionary
