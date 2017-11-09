# -*- coding: utf-8 -*-
import codecs
import numpy as np
import pymorphy2

morph = pymorphy2.MorphAnalyzer()


class FeatureMaking:
    def __init__(self, path):
        if path is None:
            path = "C:\\Users\\admin\\PycharmProjects\\ner_svm\\feature_list.txt"
        self.list_of_features_to_use = self.choose_features(path)
        self.token_id = None
        self.token_text = None
        self.position = None

    def create_features(self, word):
        self.token_id = word[0]
        self.token_text = word[2]
        self.position = word[1]

        wordvector = []

        for feature_function in self.list_of_features_to_use:
            wordvector.extend(feature_function())

        return np.array(wordvector)

    def choose_features(self, path):
        list_of_features = {'length': self.length, 'pos': self.pos, 'case': self.case, 'flection': self.flection}
        list_of_features_to_use = []
        with codecs.open(path, 'r', encoding='utf-8') as f:
            for row in f.readlines():
                row = row.split()
                if row[0] in list_of_features:
                    list_of_features_to_use.append(list_of_features[row[0]])
        return list_of_features_to_use

    def length(self):
        return [len(self.token_text)]

    def pos(self):
        parsed_word = morph.parse(self.token_text)[0]
        pos = str(parsed_word.tag.POS)
        if 'NOUN' in pos:
            return [0, 0, 0]
        elif 'VERB' in pos:
            return [0, 0, 1]
        elif 'ADJ' in pos:
            return [0, 1, 0]
        elif 'PREP' in pos:
            return [0, 1, 1]
        elif 'PNCT' in pos:
            return [1, 0, 0]
        elif 'CONJ' in pos:
            return [1, 0, 1]
        else:
            return [1, 1, 0]

    def flection(self):
        return [0, 1]

    def case(self):
        if self.token_text.isupper():
            return [0, 0]
        elif self.token_text.islower():
            return [0, 1]
        elif self.token_text.istitle():
            return [1, 0]
        else:
            return [1, 1]
