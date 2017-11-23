# -*- coding: utf-8 -*-
import texterra
#t = texterra.API('YOURKEY')
import pymorphy2
from src.enitites.features.abstract_feature import AbstractFeature

class POSFeature(AbstractFeature):
    TAGS = ['NOUN', 'VERB', 'ADJ', 'PREP', 'PNCT', 'CONJ']

    def __init__(self, pos_tags=TAGS):
        super().__init__()
        self.morph = pymorphy2.MorphAnalyzer()
        self.pos_to_position = {}
        for position in range(len(pos_tags)):
            self.pos_to_position[pos_tags[position]] = position

    def compute_vector_for(self, token, tokenlist):
        parsed_word = self.morph.parse(token.get_text())[0]
        pos = str(parsed_word.tag.POS)
        result = [0] * self.get_vector_size()
        if pos in self.pos_to_position:
            result[self.pos_to_position[pos]] = 1
        return result

    def get_vector_size(self):
        return len(self.pos_to_position)

    def __repr__(self):
        return 'part of speech'
