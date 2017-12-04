# -*- coding: utf-8 -*-
from enitites.features.abstract_feature import AbstractFeature

class PositionFeature(AbstractFeature):
    def __init__(self):
        super().__init__()

    def compute_vector_for(self, token, document):
        dict_of_pos_in_sentences = document.get_sentences()
        return [dict_of_pos_in_sentences[token.get_id()]]

    def get_vector_size(self):
        return 1

    def __repr__(self):
        return 'position in sentence'


