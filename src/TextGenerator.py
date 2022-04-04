import random
import string

from src.Lists import WordsList
from src.Lists.StructuresList import StructuresList
from src.Lists.WordSequences import WordSequences


class TextGenerator:
    def __init__(self, save_path: str):
        self.__punct = string.punctuation
        self.__punct += '—–...«»***\n“„'
        self.__save_path = save_path
        self.__text_number = 0

    def wordStructGeneration(self, word_template: list, word_list: WordsList):
        text = ''
        for sentence_template in word_template:
            for word_template in sentence_template:
                if word_template in self.__punct:
                    text += word_template + ' '
                else:
                    index = random.randint(0, len(word_list) - 1)
                    text += word_list[index].word + ' '
        self.__saveGenText(text, 'random_generation_')
        self.__text_number += 1

    def markovWordStructGeneration(self, word_template: list, word_sequences: WordSequences):
        text = ''
        for sentence_template in word_template:
            cur_word = word_sequences.startKey
            for word in sentence_template:
                cur_word, previous_word = self.__wordSelection(word_sequences, cur_word)
                if word == 'WORD':
                    text += cur_word + ' '
                else:
                    text += word + ' '
                    cur_word = word
        self.__saveGenText(text, 'markov_generation_')
        self.__text_number += 1
        return text

    def randomStruct(self, structure_list: StructuresList, sentence_quantity: int) -> list:
        counter = 0
        text_template = list()
        while counter < sentence_quantity:
            index = random.randint(0, len(structure_list) - 1)
            sentence_struct = structure_list[index].standart
            text_template.append(sentence_struct)

        return text_template

    def __wordListSelection(self, dictionary):
        punct = string.punctuation
        self.__punct += '—–...«»***\n“„'
        wordList = []
        for k, v in dictionary.items():
            if k not in punct:
                wordList += [k] * v
        return wordList

    def __wordSelection(self, word_sequences: WordSequences, current_word):
        word_list = self.__wordListSelection(word_sequences.Dictionary[current_word])
        cur_word = current_word
        if len(word_list) == 0:
            cur_word = word_sequences.startKey
            word_list = self.__wordListSelection(word_sequences.Dictionary[cur_word])
        cur_word = word_list[random.randint(0, len(word_list) - 1)]
        if cur_word == word_sequences.endKey:
            cur_word = word_sequences.startKey
        return cur_word

    def __saveGenText(self, text: str, text_name: str):
        file_name = text_name + str(self.__text_number)
        f = open(self.__save_path + file_name + '.txt', 'w', encoding='UTF-8')
        f.write(text)
        f.close()
        if self.__text_number % 100 == 0:
            print('Text ' + file_name + ' saved!')
