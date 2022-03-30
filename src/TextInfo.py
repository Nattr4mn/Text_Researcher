import json
import sys

from nltk import sent_tokenize, word_tokenize
from src.Lists.StructuresList import StructuresList
from src.Lists.WordSequences import WordSequences
from src.Lists.WordsList import WordsList
from src.Word import Word


class TextInfo:
    def __init__(self):
        self.__structures_list = StructuresList()
        self.__words_list = WordsList()
        self.__word_sequences = WordSequences()
        self.__text_templates = {'STAND': list(), 'POS': list(), 'MORPH': list()}
        self.__morphologic_dictionary = dict()
        self.__pos_dictionary = dict()
        self.__sentence_count = 0
        self.__min_sentences_count = sys.maxsize
        self.__max_sentences_count = 0
        self.__word_count = 0
        self.__min_word_count = sys.maxsize
        self.__max_word_count = 0

    @property
    def structures_list(self):
        return self.__structures_list

    @property
    def words_list(self):
        return self.__words_list

    @property
    def word_sequences(self):
        return self.__word_sequences

    @property
    def text_templates(self):
        return self.__text_templates

    @property
    def morphologic_dictionary(self):
        return self.__morphologic_dictionary

    @property
    def pos_dictionary(self):
        return self.__pos_dictionary

    @property
    def sentence_count(self):
        return self.__sentence_count

    @property
    def min_sentences_count(self):
        return self.__min_sentences_count

    @property
    def max_sentences_count(self):
        return self.__max_sentences_count

    @property
    def word_count(self):
        return self.__word_count

    @property
    def min_word_count(self):
        return self.__min_word_count

    @property
    def max_word_count(self):
        return self.__max_word_count

    def collectInformation(self, text: str):
        text_tokens, sentence_count, word_count = TextInfo.tokenizeText(text)
        text_template = {'STAND': list(), 'POS': list(), 'MORPH': list()}
        self.__sentence_count += sentence_count
        self.__word_count += word_count

        if sentence_count < self.__min_sentences_count:
            self.__min_sentences_count = sentence_count

        if sentence_count > self.__max_sentences_count:
            self.__max_sentences_count = sentence_count

        self.__word_sequences.createSequences(text_tokens)

        for sentence_token in text_tokens:
            self.__structures_list.append(sentence_token)
            text_template['STAND'].append(self.__structures_list[-1].standart)
            text_template['POS'].append(self.__structures_list[-1].pos)
            text_template['MORPH'].append(self.__structures_list[-1].morphologic)

            if len(sentence_token) < self.__min_word_count:
                self.__min_word_count = len(sentence_token)

            if len(sentence_token) > self.__max_word_count:
                self.__max_word_count = len(sentence_token)

            for word_token in sentence_token:
                self.__words_list.append(word_token)
                word = self.__words_list[-1]
                self.__updateMorphologicDictionary(word)

        self.__text_templates['STAND'].append(text_template['STAND'])
        self.__text_templates['POS'].append(text_template['POS'])
        self.__text_templates['MORPH'].append(text_template['MORPH'])

    def saveInfo(self, file_name="TextInfo"):
        self.__structures_list.save()
        self.__words_list.save()
        self.__word_sequences.save()
        morph_dict = dict()
        for key, value in self.__morphologic_dictionary.items():
            morph_dict.setdefault(key, list(value))

        with open(str(file_name) + ".json", "w") as file:
            save_data = [self.__text_templates, morph_dict, self.__sentence_count, self.__word_count,
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
        word_count = 0
        for token in tokens:
            word_count += len(token)
        return tokens, sentence_count, word_count

    def __updateMorphologicDictionary(self, word: Word):
        if self.__morphologic_dictionary.get(str(word.characteristic)) is None:
            self.__morphologic_dictionary.update({str(word.characteristic): set(word.word)})
        else:
            self.__morphologic_dictionary[str(word.characteristic)].add(word.word)

        if self.__pos_dictionary.get(str(word.characteristic[0])) is None:
            self.__pos_dictionary.update({str(word.characteristic[0]): set(word.word)})
        else:
            self.__pos_dictionary[str(word.characteristic[0])].add(word.word)
