# -*- coding: utf-8 -*-
import pymorphy2

morph = pymorphy2.MorphAnalyzer()
from src.enitites.features.morpho_case import MorphoFeature

# XXX duplicates NextMorphoCaseFeature
class PrevMorphoCaseFeature(MorphoFeature):
    def __init__(self):
        super().__init__()

    def compute_vector_for(self, token, document):
        current_index = document.index(token)
        if current_index != 0:
            prev_token = document[current_index - 1]
            return self._count_morpho_vector(prev_token)
        else:
            return [1, 0, 1, 1]

    def __repr__(self):
        return 'prev_morpho_case'