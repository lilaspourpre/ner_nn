# -*- coding: utf-8 -*-
import texterra
#t = texterra.API('YOURKEY')
import pymorphy2
morph = pymorphy2.MorphAnalyzer()
from src.enitites.features.abstract_feature import AbstractFeature

class POSFeature(AbstractFeature):
    def __init__(self, taglist=None):
        super().__init__()
        if taglist is None:
            self.TAGS = ['NOUN', 'VERB', 'ADJ', 'PREP', 'PNCT', 'CONJ']
        else:
            self.TAGS = taglist

    def compute_vector_for(self, token, tokenlist):
        parsed_word = morph.parse(token.get_text())[0]
        pos = str(parsed_word.tag.POS)
        result = []
        for tag in self.TAGS:
            result.append(1)  if tag in pos else result.append(0)
        return result

    def get_vector_size(self):
        return len(self.TAGS)

    def __repr__(self):
        return 'part of speech'
