# -*- coding: utf-8 -*-
import pymorphy2

# XXX bad idea. Why not use it as class property?
morph = pymorphy2.MorphAnalyzer()
from src.enitites.features.abstract_feature import AbstractFeature


class MorphoFeature(AbstractFeature):
    def __init__(self):
        super().__init__()

    def compute_vector_for(self, token, document):
        return self._count_morpho_vector(token)

    def _count_morpho_vector(self, token):
        parsed_word = morph.parse(token.get_text())[0]
        case = str(parsed_word.tag.case)
        # XXX bad encoding idea
        if 'nomn' in case:
            return [0, 0, 0, 0]
        elif 'gent' in case:
            return [0, 0, 0, 1]
        elif 'datv' in case:
            return [0, 0, 1, 0]
        elif 'accs' in case:
            return [0, 0, 1, 1]
        elif 'ablt' in case:
            return [0, 1, 0, 0]
        elif 'loct' in case:
            return [0, 1, 0, 1]
        elif 'voct' in case:
            return [0, 1, 1, 0]
        elif 'gen2' in case:
            return [0, 1, 1, 1]
        elif 'acc2' in case:
            return [1, 0, 0, 0]
        elif 'loc2' in case:
            return [1, 0, 0, 1]
        else:
            return [1, 0, 1, 0]


    def __repr__(self):
        return 'morphological case'
