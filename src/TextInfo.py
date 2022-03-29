import json
import sys

from nltk import sent_tokenize, word_tokenize
from Lists.StructuresList import StructuresList
from Lists.WordSequences import WordSequences
from Lists.WordsList import WordsList


class TextInfo:
    def __init__(self):
        self.__structures_list = StructuresList()
        self.__words_list = WordsList()
        self.__word_sequences = WordSequences()
        self.__text_templates = {'STAND': list(), 'POS': list(), 'MORPH': list()}
        self.__morphologic_dictionary = dict()
        self.__sentence_count = 0
        self.__min_sentences_count = sys.maxsize
        self.__max_sentences_count = 0
        self.__word_count = 0
        self.__min_word_count = sys.maxsize
        self.__max_word_count = 0

    def collectInformation(self, text: str):
        text_tokens, sentence_count, word_count = TextInfo.tokenizeText(text)
        text_template = {'STAND': list(), 'POS': list(), 'MORPH': list()}
        self.__sentence_count += sentence_count
        self.__word_count += word_count

        if sentence_count < self.__min_sentences_count:
            self.__min_sentences_count = sentence_count
        elif sentence_count > self.__max_sentences_count:
            self.__max_sentences_count = sentence_count

        self.__word_sequences.createSequences(text_tokens)

        for sentence_token in text_tokens:
            self.__structures_list.append(sentence_token)
            text_template['STAND'].append(self.__structures_list[-1].standart)
            text_template['POS'].append(self.__structures_list[-1].pos)
            text_template['MORPH'].append(self.__structures_list[-1].morphologic)

            if len(sentence_token) < self.__min_word_count:
                self.__min_word_count = len(sentence_token)
            elif len(sentence_token) > self.__max_word_count:
                self.__max_word_count = len(sentence_token)

            for word_token in sentence_token:
                self.__words_list.append(word_token)
                word = self.__words_list[-1]

                if self.__morphologic_dictionary.get(word.characteristic) is None:
                    self.__morphologic_dictionary.update({word.characteristic, set(word.word)})
                else:
                    self.__morphologic_dictionary[word.characteristic].add(word.word)

        self.__text_templates['STAND'].append(text_template['STAND'])
        self.__text_templates['POS'].append(text_template['POS'])
        self.__text_templates['MORPH'].append(text_template['MORPH'])

    def saveInfo(self, file_name="TextInfo"):
        self.__structures_list.save()
        self.__words_list.save()
        self.__word_sequences.save()
        with open(str(file_name) + ".json", "w") as file:
            save_data = [self.__text_templates, self.__morphologic_dictionary, self.__sentence_count, self.__word_count,
                         self.__min_sentences_count, self.__max_sentences_count, self.__min_word_count, self.__max_word_count]
            json.dump(save_data, file)

    def loadInfo(self, file_name="TextInfo"):
        self.__structures_list.load()
        self.__words_list.load()
        self.__word_sequences.load()
        with open(str(file_name) + ".json", "r") as file:
            load_data = json.load(file)
        self.__text_templates = load_data[0]
        self.__morphologic_dictionary = load_data[1]
        self.__sentence_count = int(load_data[2])
        self.__word_count = int(load_data[3])
        self.__min_sentences_count = int(load_data[4])
        self.__max_sentences_count = int(load_data[5])
        self.__min_word_count = int(load_data[6])
        self.__max_word_count = int(load_data[7])

    @staticmethod
    def tokenizeText(text: str):
        text = text.lower()
        tokens = sent_tokenize(text, language="russian")
        sentence_count = len(tokens)
        tokens = [word_tokenize(sentence, language="russian") for sentence in tokens]
        word_count = len(tokens)
        return tokens, sentence_count, word_count
