import json
import string
import pymorphy2

from src.Statistics.GraphBuilder import GraphBuilder
from src.Statistics.Statistics import Statistics
from src.TextInfo import TextInfo


class StatisticalData:
    def __init__(self):
        self.__texts_statistic = []
        self.__pos_counter = dict()
        self.__counter_pos_text = dict()
        self.__sentence_count = 0
        self.__word_count = 0

    @property
    def texts_statistic(self):
        return self.__texts_statistic

    @property
    def pos_counter(self):
        return self.__pos_counter

    @property
    def counter_pos_text(self):
        return self.__counter_pos_text

    @property
    def sentence_count(self):
        return self.__sentence_count

    @property
    def word_count(self):
        return self.__word_count

    def calculateStatistics(self, text: str):
        text_tokens, sentence_count, word_count = TextInfo.tokenizeText(text)
        self.__sentence_count += sentence_count
        self.__word_count += word_count
        pos_structure = self.__createPOSStructure(text_tokens)
        graph = GraphBuilder()
        graph.createGraph(pos_structure)
        statistics = Statistics()
        statistics.calculate(graph.graph, sentence_count)
        self.__texts_statistic.append(statistics)
        return statistics, sentence_count

    def save(self, file_name="StatisticalData"):
        try:
            with open(str(file_name) + ".json", "w") as write_file:
                save_data = []
                value_list = [value.toList() for value in self.__texts_statistic]
                save_data.append(value_list)
                save_data.append(self.__pos_counter)
                save_data.append(self.__counter_pos_text)
                save_data.append(self.__sentence_count)
                save_data.append(self.__word_count)
                json.dump(save_data, write_file)
        except Exception:
            print('An error occurred while saving the StatisticsData!')

    def load(self, file_name="StatisticalData"):
        try:
            with open(str(file_name) + ".json", "r") as read_file:
                load_data = json.load(read_file)

            for data in load_data[0]:
                statistics = Statistics()
                statistics.toStatistics(data)
                self.__texts_statistic.append(statistics)
            self.__pos_counter = load_data[1]
            self.__counter_pos_text  = load_data[2]
            self.__sentence_count = load_data[3]
            self.__word_count = load_data[4]
        except Exception:
            print('An error occurred while loading the list of StatisticsData!')

    def __createPOSStructure(self, text_tokens: list) -> list:
        morph = pymorphy2.MorphAnalyzer()
        pos_structure = []
        pos_counter = dict()
        punctuation = string.punctuation
        punctuation += '—–...«»***\n '
        for sentense_token in text_tokens:
            pos_sentence_structure = []
            for word_token in sentense_token:
                if word_token not in punctuation:
                    word_info = morph.parse(word_token)[0]
                    word_pos = str(word_info.tag.POS)
                    pos_sentence_structure.append(word_pos)
                    if pos_counter.get(word_pos) is None:
                        pos_counter[word_pos] = 1
                    else:
                        pos_counter[word_pos] += 1
            pos_structure.append(pos_sentence_structure)
        self.__addPOSCounter(pos_counter)
        return pos_structure

    def __addPOSCounter(self, pos_counter: dict):
        for key, value in pos_counter.items():
            if self.__counter_pos_text.get(key) is None:
                self.__counter_pos_text[key] = [value]
            else:
                self.__counter_pos_text[key].append(value)

            if self.__pos_counter.get(key) is None:
                self.__pos_counter[key] = value
            else:
                self.__pos_counter[key] += value