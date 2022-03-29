import os
import pickle
import pymorphy2 as pm


class WordSequences:
    def __init__(self, startKey='@START', endKey='@END'):
        self.__dictionary = {}
        self.__wordCount = 0
        self.__startKey = startKey
        self.__endKey = endKey

    @property
    def Dictionary(self):
        return self.__dictionary

    def createSequences(self, text_tokens: list):
        for sentence in range(len(text_tokens)):
            self.__addWord(self.__startKey, text_tokens[sentence][0])

            for word in range(len(text_tokens[sentence]) - 1):
                self.__addWord(text_tokens[sentence][word], text_tokens[sentence][word + 1])

            self.__addWord(text_tokens[sentence][len(text_tokens[sentence]) - 1], self.__endKey)

    def endKey(self):
        return self.__endKey

    def load(self, file_name='WordSequences'):
        if os.path.exists(str(file_name) + '.pickle'):
            with open('dictionary.pickle', 'rb') as file:
                self.__dictionary = pickle.load(file)

    def save(self, file_name='WordSequences'):
        with open(str(file_name) + '.pickle', 'wb') as file:
            pickle.dump(self.__dictionary, file)

    def startKey(self):
        return self.__startKey

    def __addWord(self, curWord, nextWord):
        morph = pm.MorphAnalyzer()
        if curWord in self.__dictionary:
            if nextWord in self.__dictionary[curWord]:
                self.__dictionary[curWord][nextWord] += 1
            elif str(morph.parse(nextWord)[0].tag) != 'PNCT':
                self.__dictionary[curWord][nextWord] = 1
        else:
            if str(morph.parse(nextWord)[0].tag) != 'PNCT':
                self.__dictionary[curWord] = {nextWord: 1}
            else:
                self.__dictionary[curWord] = {}
