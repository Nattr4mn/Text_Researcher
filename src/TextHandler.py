import re
from chardet import UniversalDetector
from nltk import sent_tokenize, word_tokenize


class TextHandler:
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