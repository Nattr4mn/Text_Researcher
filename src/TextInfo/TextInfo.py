import json
import sys
import pymorphy2

from nltk import sent_tokenize
from razdel import tokenize

from src.TextInfo.StructuresList import StructuresList
from src.TextInfo.WordSequences import WordSequences
from src.TextInfo.WordsList import WordsList
from src.TextInfo.Word import Word


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
        self.__sentence_count += sentence_count
        self.__word_count += word_count
        if sentence_count < self.__min_sentences_count:
            self.__min_sentences_count = sentence_count
        if sentence_count > self.__max_sentences_count:
            self.__max_sentences_count = sentence_count
        self.__tokensProcessing(text_tokens)

    def saveInfo(self, file_name="TextInfo"):
        self.__structures_list.save()
        self.__words_list.save()
        self.__word_sequences.save()
        for key, value in self.__morphologic_dictionary.items():
            self.__morphologic_dictionary[str(key)] = list(set(value))
        for key, value in self.__pos_dictionary.items():
            self.__pos_dictionary[str(key)] = list(set(value))
        with open(str(file_name) + ".json", "w") as file:
            save_data = [self.__text_templates, self.__morphologic_dictionary, self.__pos_dictionary, self.__sentence_count, self.__word_count,
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
        self.__pos_dictionary = load_data[2]
        self.__sentence_count = int(load_data[3])
        self.__word_count = int(load_data[4])
        self.__min_sentences_count = int(load_data[5])
        self.__max_sentences_count = int(load_data[6])
        self.__min_word_count = int(load_data[7])
        self.__max_word_count = int(load_data[8])

    @staticmethod
    def tokenizeText(text: str):
        text = text.lower()
        sentence_tokens = sent_tokenize(text, language="russian")
        sentence_count = len(sentence_tokens)
        word_count = 0
        text_tokens = []
        for sentence_token in sentence_tokens:
            word_tokens = list(tokenize(sentence_token.lower()))          #Токенизация по словам
            text_tokens.append([_.text for _ in word_tokens])
            word_count += len(word_tokens)
        return text_tokens, sentence_count, word_count

    def __tokensProcessing(self, text_tokens: list):
        morph = pymorphy2.MorphAnalyzer()
        text_template = {'STAND': list(), 'POS': list(), 'MORPH': list()}

        for sentence_token in text_tokens:
            sentence_info = list()
            for word_token in sentence_token:
                word_info = morph.parse(word_token)[0]
                sentence_info.append(word_info)
                self.__words_list.append(word_info)
                word = self.__words_list[-1]
                self.__updateMorphologicDictionary(word)

            self.__word_sequences.createSequences(sentence_info)
            self.__structures_list.append(sentence_info)
            text_template['STAND'].append(self.__structures_list[-1].standart)
            text_template['POS'].append(self.__structures_list[-1].pos)
            text_template['MORPH'].append(self.__structures_list[-1].morphologic)

            if len(sentence_token) < self.__min_word_count:
                self.__min_word_count = len(sentence_token)

            if len(sentence_token) > self.__max_word_count:
                self.__max_word_count = len(sentence_token)

        self.__addTemplates(text_template['STAND'], text_template['POS'], text_template['MORPH'])

    def __addTemplates(self, standart_template: list, pos_template: list, morph_template: list):
        if standart_template not in self.__text_templates['STAND']:
            self.__text_templates['STAND'].append(standart_template)
        if pos_template not in self.__text_templates['STAND']:
            self.__text_templates['POS'].append(pos_template)
        if morph_template not in self.__text_templates['STAND']:
            self.__text_templates['MORPH'].append(morph_template)

    def __updateMorphologicDictionary(self, word: Word):
        if self.__morphologic_dictionary.get(str(word.characteristic)) is None:
            self.__morphologic_dictionary.update({str(word.characteristic): [word.word]})
        else:
            self.__morphologic_dictionary[str(word.characteristic)].append(word.word)

        if self.__pos_dictionary.get(str(word.characteristic[0])) is None:
            self.__pos_dictionary.update({str(word.characteristic[0]): [word.word]})
        else:
            self.__pos_dictionary[str(word.characteristic[0])].append(word.word)
