# -*- coding: utf-8 -*-
import pymorphy2

from src.enitites.features.abstract_feature import AbstractFeature


class MorphoFeature(AbstractFeature):
    def __init__(self, cases_to_detect=None):
        super().__init__()
        self.morph = pymorphy2.MorphAnalyzer()
        if cases_to_detect is None:
            self.CASES = ['nomn', 'gent', 'datv', 'accs', 'ablt', 'loct', 'voct', 'gen2', 'acc2', 'loc2']
        else:
            self.CASES = cases_to_detect

    def compute_vector_for(self, token, tokenlist):
        parsed_word = self.morph.parse(token.get_text())[0]
        current_case = str(parsed_word.tag.case)
        result = []
        for case in self.CASES:
            result.append(1) if case in current_case else result.append(0)
        return result

    def get_vector_size(self):
        return len(self.CASES)

    def __repr__(self):
        return 'morphological case'
