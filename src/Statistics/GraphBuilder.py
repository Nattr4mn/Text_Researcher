import string

import numpy as np
import pymorphy2


class GraphBuilder:
    def __init__(self):
        self.__graph = None
        self.__graphSize = 0

    @property
    def graph(self):
        return self.__graph

    def createGraph(self, text_tokens: list):
        pos_tokens = self.__createStructure(text_tokens)
        dictionary = self.__createDictionary(pos_tokens)
        self.__graph = np.zeros((self.__graphSize, self.__graphSize))
        for sentence in text_tokens:
            for word in sentence:
                for other_words in sentence:
                    if other_words != word:
                        self.__graph[dictionary[word]][dictionary[other_words]] += 1
        return self.__graph

    def __createStructure(self, text_tokens):
        morph = pymorphy2.MorphAnalyzer()
        punctuation = string.punctuation
        punctuation += '—–...«»***\n '
        pos_tokens = []
        for sentence_token in text_tokens:
            pos_sentence_tokens = []
            for word_token in sentence_token:
                if word_token not in punctuation:
                    word = morph.parse(word_token)[0]
                    word_pos = str(word.tag.POS)
                    pos_sentence_tokens.append(word_pos)
            pos_tokens.append(pos_sentence_tokens)
        return pos_tokens

    def __createDictionary(self, tokens):
        dictionary = {}
        for sentence in range(len(tokens)):
            self.__addWord(tokens[sentence], dictionary)
        return dictionary

    def __addWord(self, sentenceTokens, dictionary):
        for word in sentenceTokens:
            if word not in dictionary:
                dictionary[word] = self.__graphSize
                self.__graphSize += 1
