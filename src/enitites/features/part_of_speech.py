# -*- coding: utf-8 -*-
import texterra
#t = texterra.API('YOURKEY')
import pymorphy2
morph = pymorphy2.MorphAnalyzer()
from src.enitites.features.abstract_feature import AbstractFeature

class POSFeature(AbstractFeature):
    def __init__(self):
        super().__init__()

    def compute_vector_for(self, token, document):
        return self._count_pos_vector(token)

    def _count_pos_vector(self, token):
        parsed_word = morph.parse(token.get_text())[0]
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

    def __repr__(self):
        return 'part of speech'
