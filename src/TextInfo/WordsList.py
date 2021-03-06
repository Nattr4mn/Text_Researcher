import collections
import json

from pymorphy2.analyzer import Parse
from src.TextInfo.Word import Word


class WordsList(collections.MutableSequence):
    def __init__(self, *args):
        self.__words = list()
        self.__index_table = dict()
        self.extend(list(args))

    def __len__(self):
        return len(self.__words)

    def __getitem__(self, i: int):
        return self.__words[i]

    def clear(self):
        self.__words.clear()
        self.__index_table.clear()

    def __delitem__(self, i):
        self.__index_table.pop(self.__words[i].word)
        del self.__words[i]

    def __str__(self):
        return '; '.join([str(word.toList()) for word in self.__words])

    def __setitem__(self, i, word: Word):
        self.__index_table.pop(self.__words[i].word)
        self.__index_table.update({word.word: i})
        self.__words[i] = word

    def __contains__(self, word: str):
        if self.__index_table.get(word) is not None:
            return True
        else:
            return False

    def insert(self, i, word_info: Parse):
        index = self.__index_table.get(word_info.word)
        if index is not None:
            self.__words[index].count += 1
        else:
            wordInfo = Word()
            wordInfo.parse(word_info)
            if wordInfo.characteristic[0] is not 'PNCT':
                self.__words.append(wordInfo)
                self.__index_table.update({word_info.word: len(self.__words) - 1})

    def save(self, file_name="WordsList"):
        with open(str(file_name) + ".json", "w") as write_file:
            save_data = []
            value_list = [value.toList() for value in self.__words]
            save_data.append(value_list)
            save_data.append(self.__index_table)
            json.dump(save_data, write_file)

    def load(self, file_name="WordsList"):
        with open(str(file_name) + ".json", "r") as read_file:
            load_data = json.load(read_file)

        self.__words = [Word.toWord(word) for word in load_data[0]]
        self.__index_table = load_data[1]
