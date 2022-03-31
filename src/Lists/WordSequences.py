import json

from pymorphy2.analyzer import Parse


class WordSequences:
    def __init__(self, startKey='@START', endKey='@END'):
        self.__dictionary = {}
        self.__wordCount = 0
        self.__startKey = startKey
        self.__endKey = endKey

    @property
    def Dictionary(self):
        return self.__dictionary

    @property
    def startKey(self):
        return self.__startKey

    @property
    def endKey(self):
        return self.__endKey

    def createSequences(self, sentence_info: list):
        self.__addWord(self.__startKey, sentence_info[0])

        for word in range(len(sentence_info) - 1):
            self.__addWord(sentence_info[word].word, sentence_info[word + 1])

        if sentence_info[-1].word in self.__dictionary:
            if self.__endKey in self.__dictionary[sentence_info[-1].word]:
                self.__dictionary[sentence_info[-1].word][self.__endKey] += 1
            else:
                self.__dictionary[sentence_info[-1].word][self.__endKey] = 1
        else:
            self.__dictionary[sentence_info[-1].word] = {self.__endKey: 1}

    def save(self, file_name="WordSequences"):
        with open(str(file_name) + ".json", "w") as write_file:
            save_data = [self.__dictionary, self.__wordCount]
            json.dump(save_data, write_file)

    def load(self, file_name="WordSequences"):
        with open(str(file_name) + ".json", "r") as read_file:
            load_data = json.load(read_file)
        self.__dictionary = load_data[0]
        self.__wordCount = load_data[1]

    def __addWord(self, curWord: str, nextWord: Parse):
        if curWord in self.__dictionary:
            if nextWord.word in self.__dictionary[curWord]:
                self.__dictionary[curWord][nextWord.word] += 1
            elif str(nextWord.tag) != 'PNCT':
                self.__dictionary[curWord][nextWord.word] = 1
        else:
            if str(nextWord.tag) != 'PNCT':
                self.__dictionary[curWord] = {nextWord.word: 1}
            else:
                self.__dictionary[curWord] = {}
