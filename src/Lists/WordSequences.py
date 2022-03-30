import json
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

    def save(self, file_name="WordSequences"):
        try:
            with open(str(file_name) + ".json", "w") as write_file:
                save_data = [self.__dictionary, self.__wordCount]
                json.dump(save_data, write_file)
        except Exception:
            print('An error occurred while saving the WordSequences!')

    def load(self, file_name="WordSequences"):
        try:
            with open(str(file_name) + ".json", "r") as read_file:
                load_data = json.load(read_file)

            self.__dictionary = load_data[0]
            self.__wordCount = load_data[1]
        except Exception:
            print('An error occurred while loading the list of WordSequences!')

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
