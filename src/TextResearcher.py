import os
import re
import sys

import numpy as np
from chardet import UniversalDetector

from src.Statistics.PlotBuilder import PlotBuilder
from src.Statistics.StatisticalData import StatisticalData
from src.TextInfo import TextInfo


class TextResearcher:
    def __init__(self, process_before_saving=100):
        self.__text_info = TextInfo()
        self.__process_before_saving = process_before_saving
        self.__natural_statistic_data = StatisticalData()
        self.__generate_statistic_data = StatisticalData()
        self.__plot = PlotBuilder()
        self.__textCount = 0

    @property
    def text_info(self):
        return self.__text_info

    def collectingTextInfo(self, text: str):
        self.__text_info.collectInformation(text)

    def researchCorpuses(self, natural_text_path: str, generation_text_path: str):
        np.set_printoptions(threshold=sys.maxsize)
        natural_file_list = os.listdir(natural_text_path)
        gen_file_list = os.listdir(generation_text_path)
        for file_index in range(0, len(gen_file_list)):
            try:
                nat_current_file = natural_text_path + '\\' + natural_file_list[file_index]
                gen_current_file = generation_text_path + '\\' + gen_file_list[file_index]

                encoding = TextResearcher.determineEncoding(nat_current_file)
                with open(nat_current_file, encoding=encoding) as document:
                    nat_text = document.read()

                encoding = TextResearcher.determineEncoding(gen_current_file)
                with open(gen_current_file, encoding=encoding) as document:
                    gen_text = document.read()

                nat_statistic, nat_sentence_count = self.__natural_statistic_data.calculateStatistics(nat_text)
                gen_statistic, gen_sentence_count = self.__generate_statistic_data.calculateStatistics(gen_text)

                if self.__textCount % self.__process_before_saving == 0:
                    self.__natural_statistic_data.save('Natural_Statistic_Data')
                    self.__generate_statistic_data.save('Generation_Statistic_Data')
                    print("Обработано: " + str(self.__textCount))

                self.__plot.statisticsComp(nat_statistic, gen_statistic)
                self.__textCount += 1
            except Exception as e:
                print('An error occurred while processing the file: ' + str(natural_file_list[file_index]) + '; ' + str(gen_file_list[file_index]))
                print(e)
                continue
        self.__natural_statistic_data.save('Natural_Statistic_Data')
        self.__generate_statistic_data.save('Generation_Statistic_Data')
        self.__buildPlots()

    def collectingTextInfoInCorpus(self, corpus_path: str):
        if re.match(r"\S:\\\S*", corpus_path) is None:
            raise ValueError("Invalid path!")
        file_list = os.listdir(corpus_path)
        save_counter = 0
        for file_name in file_list:
            try:
                current_file = corpus_path + '\\' + file_name
                encoding = TextResearcher.determineEncoding(current_file)
                with open(current_file, encoding=encoding) as document:
                    text = document.read()
                self.__text_info.collectInformation(text)

                save_counter += 1
                if save_counter == self.__process_before_saving:
                    self.__text_info.saveInfo()
                    print('Saved! Last processed file: ' + file_name)
                    save_counter = 0
            except Exception as e:
                print('An error occurred while processing the file ' + file_name)
                print(e)
                continue
        self.__text_info.saveInfo()

    def loadData(self):
        self.__text_info.loadInfo()
        self.__natural_statistic_data.load('Natural_Statistic_Data')
        self.__generate_statistic_data.load('Generation_Statistic_Data')

    @staticmethod
    def determineEncoding(path: str):
        if re.match(r"\S:\\\S*", path) == None:
            raise ValueError("Invalid path!")
        detector = UniversalDetector()
        with open(path, 'rb') as fh:
            for line in fh:
                detector.feed(line)
                if detector.done:
                    break
            detector.close()
        return detector.result['encoding']

    def __buildPlots(self, plotNameForSave=''):
        self.__plot.CreatePlots(self.__textCount, plotNameForSave)
        self.__plot.CreatePlotsAV(self.__textCount, plotNameForSave)
        self.__plot.CreatePlotsSTD(plotNameForSave)
        self.__plot.CreatePlotsSTDmean(plotNameForSave)