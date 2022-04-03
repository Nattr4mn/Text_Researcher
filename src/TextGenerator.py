import random
import string

from src.Lists import WordsList
from src.Lists.StructuresList import StructuresList
from src.Lists.WordSequences import WordSequences


class TextGenerator:
    def __init__(self, save_path: str):
        self.__punct = string.punctuation
        self.__punct += '—–...«»***\n '
        self.__save_path = save_path
        self.__text_number = 0

    def wordStructGeneration(self, word_template: list, word_list: WordsList):
        text = ''
        for sentence_template in word_template:
            for word_template in sentence_template:
                if word_template in self.__punct:
                    text += word_template
                else:
                    index = random.randint(0, len(word_list) - 1)
                    text += ' ' + word_list[index].word
        self.__saveGenText(text, 'word_template_')
        self.__text_number += 1

    def markovWordStructGeneration(self, word_template: list, word_sequences: WordSequences):
        text = ''
        curWord = previousWord = word_sequences.startKey

        for sentence_template in word_template:
            for word in sentence_template:
                if word == 'WORD':
                    text += word + ' '
                    curWord, previousWord = self.__WordSelection(word, word)
                else:
                    curWord, previousWord = self.__WordSelection(curWord, previousWord)
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

    def __WordListSelection(self, dictionary):
        punct = string.punctuation
        punct += '—–...«»***\n '
        wordList = []

        for k, v in dictionary.items():
            if k not in punct:
                wordList += [k] * v

        return wordList

    def __WordSelection(self, word_sequences: WordSequences, curWord, previousWord):
        wordList = self.__WordListSelection(word_sequences.Dictionary[curWord])
        if len(wordList) == 0:
            while len(wordList) == 0:
                curWord = previousWord
                wordList = self.__WordListSelection(word_sequences.Dictionary[curWord])
        previousWord = curWord
        curWord = wordList[random.randint(0, len(wordList) - 1)]
        if curWord == word_sequences.endKey():
            curWord = previousWord = word_sequences.startKey()
        else:
            self.__text += curWord + ' '

        return curWord, previousWord

    def __saveGenText(self, text: str, text_name: str):
        file_name = text_name + str(self.__text_number)
        f = open(self.__save_path + file_name, 'w', encoding='UTF-8')
        f.write(text)
        f.close()
        print('Text ' + file_name + ' saved!')