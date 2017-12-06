# -*- coding: utf-8 -*-
import pymorphy2
from nltk.tokenize import sent_tokenize


# TODO: all (suf and pref to parameter in vector)
class Document:
    def __init__(self, list_of_tagged_tokens, morph_analyzer=pymorphy2.MorphAnalyzer()):
        self.morph = morph_analyzer
        self.__list_of_tagged_tokens = list_of_tagged_tokens
        self.__list_of_tokens = self.__compute_tokens()
        self.__dict_of_parsed_tokens = self.__compute_morpho_parsed_tokens()
        self.__list_of_sentences = self.__compute_sentences()
        self.__token_text_by_id = self.__compute_token_texts_by_id()
        self.__token_text_by_index = self.__compute_token_texts_by_index()
        self.__id_by_tokens = self.__compute_id_by_tokens()
        self.__index_by_tokens = self.__compute_index_by_tokens()
        self.__id_by_index = self.__compute_id_by_index()
        self.__token_texts = self.__compute_token_texts()

    def get_tagged_tokens(self):
        return self.__list_of_tagged_tokens

    def get_tokens(self):
        return self.__list_of_tokens

    def get_morpho_parsed_tokens(self):
        return self.__dict_of_parsed_tokens

    def get_sentences(self):
        return self.__list_of_sentences

    def get_token_texts(self):
        return self.__token_texts

    def get_token_text_by_id(self, token_id):
        return self.__token_text_by_id[token_id]

    def get_token_text_by_index(self, index):
        return self.__token_text_by_index[index]

    def get_id_by_token(self, token):
        return self.__id_by_tokens[token]

    def get_index_by_token(self, token):
        return self.__index_by_tokens[token]

    def get_id_by_index(self, index):
        return self.__id_by_index[index]

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

    def __compute_token_texts_by_id(self):
        tokens_by_id = {}
        for i in self.get_tokens():
            tokens_by_id[i.get_id()] = i.get_text()
        return tokens_by_id

    def __compute_token_texts_by_index(self):
        tokens_by_index = {}
        tokens = self.get_tokens()
        for i in range(len(tokens)):
            tokens_by_index[i] = tokens[i].get_text()
        return tokens_by_index

    def __compute_id_by_tokens(self):
        id_by_tokens = {}
        tokens = self.get_tokens()
        for token in tokens:
            id_by_tokens[token] = token.get_id()
        return id_by_tokens

    def __compute_index_by_tokens(self):
        index_by_tokens = {}
        tokens = self.get_tokens()
        for i in range(len(tokens)):
            index_by_tokens[tokens[i]] = i
        return index_by_tokens

    def __compute_id_by_index(self):
        id_by_index = {}
        tokens = self.get_tokens()
        for i in range(len(tokens)):
            id_by_index[i] = tokens[i].get_id()
        return id_by_index

    def __compute_token_texts(self):
        return list(self.__token_text_by_id.values())

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
            for i in range(len(sent_split) - 1):
                dict_of_pos_in_sentences[list_of_all_ids[index + i]] = i
            dict_of_pos_in_sentences[list_of_all_ids[index + len(sent_split) - 1]] = -1
            index += len(sent_split)
        return dict_of_pos_in_sentences
