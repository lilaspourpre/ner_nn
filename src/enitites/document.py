# -*- coding: utf-8 -*-
import pymorphy2
from nltk.tokenize import sent_tokenize

class Document:
    def __init__(self, list_of_tagged_tokens):
        self.morph = pymorphy2.MorphAnalyzer() # XXX not a good idea to keep analyzer here. I'd expect this information come as parameter
        self.__list_of_tagged_tokens = list_of_tagged_tokens
        self.__list_of_tokens = self.__compute_tokens()
        self.__dict_of_parsed_tokens = self.__compute_morpho_parsed_tokens()
        self.__list_of_sentences = self.__compute_sentences()

    def get_tagged_tokens(self):
        return self.__list_of_tagged_tokens

    def get_tokens(self):
        return self.__list_of_tokens

    def get_morpho_parsed_tokens(self):
        return self.__dict_of_parsed_tokens

    def get_sentences(self):
        return self.__list_of_sentences

    def __compute_tokens(self):
        tokens = []
        for tagged_token in self.__list_of_tagged_tokens:
            tokens.append(tagged_token.get_token())
        return tokens

    def __compute_morpho_parsed_tokens(self):
        dict_of_parsed_words = {}
        for token in self.__list_of_tokens:
            parsed_word = self.morph.parse(token.get_text())[0]
            dict_of_parsed_words[token.get_id()] = parsed_word
        return dict_of_parsed_words

    # XXX actually, this info is within input file. No need to recompute it, especially with nltk
    def __compute_sentences(self):
        # https://github.com/mhq/train_punkt/blob/master/russian.pickle
        list_of_all_words = [t.get_text() for t in self.get_tokens()]
        list_of_all_ids = [t.get_id() for t in self.get_tokens()]
        dict_of_pos_in_sentences = {}
        sent_tokenize_list = sent_tokenize(' '.join(list_of_all_words), language='russian')
        index = 0
        for sent in sent_tokenize_list:
            sent_split = sent.split()
            for i in range(len(sent_split)):
                dict_of_pos_in_sentences[list_of_all_ids[index + i]] = i
            index += len(sent_split)
        return dict_of_pos_in_sentences




