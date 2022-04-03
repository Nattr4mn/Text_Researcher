import os
import re

from chardet import UniversalDetector
from src.TextInfo import TextInfo


class TextResearcher:
    def __init__(self, process_before_saving=100):
        self.__text_info = TextInfo()
        self.__process_before_saving = process_before_saving

    @property
    def text_info(self):
        return self.__text_info

    def collectingTextInfo(self, text: str):
        self.__text_info.collectInformation(text)

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
                    self.save()
                    print('Saved! Last processed file: ' + file_name)
                    save_counter = 0
            except Exception:
                print('An error occurred while processing the file ' + file_name)
                continue

    def save(self):
        self.__text_info.saveInfo()

    def load(self):
        self.__text_info.loadInfo()

    @staticmethod
    def determineEncoding(path : str):
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