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
        self.__word_count = 0

    def collectInformation(self, text: str):
        text_tokens, sentence_count, word_count = TextInfo.tokenizeText(text)
        text_template = {'STAND': list(), 'POS': list(), 'MORPH': list()}
        self.__sentence_count += sentence_count
        self.__word_count += word_count

        self.__word_sequences.createSequences(text_tokens)

        for sentence_token in text_tokens:
            self.__structures_list.append(sentence_token)
            text_template['STAND'].append(self.__structures_list[-1].standart)
            text_template['POS'].append(self.__structures_list[-1].pos)
            text_template['MORPH'].append(self.__structures_list[-1].morphologic)

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

    @staticmethod
    def tokenizeText(text: str):
        text = text.lower()
        tokens = sent_tokenize(text, language="russian")
        sentence_count = len(tokens)
        tokens = [word_tokenize(sentence, language="russian") for sentence in tokens]
        word_count = len(tokens)
        return tokens, sentence_count, word_count
