# -*- coding: utf-8 -*-
import pymorphy2

from src.enitites.features.abstract_feature import AbstractFeature


class MorphoFeature(AbstractFeature):
    CASES = ('nomn', 'gent', 'datv', 'accs', 'ablt', 'loct', 'voct', 'gen2', 'acc2', 'loc2')
    
    def __init__(self, cases_to_detect=CASES):
        super().__init__()
        self.morph = pymorphy2.MorphAnalyzer()
        self.case_to_position = {}
        for position in range(len(cases_to_detect)):
            self.case_to_position[cases_to_detect[position]] = position

    def compute_vector_for(self, token, tokenlist):
        parsed_word = self.morph.parse(token.get_text())[0]
        current_case = str(parsed_word.tag.case)
        result = [0] * self.get_vector_size()
        if current_case in self.case_to_position:
            result[self.case_to_position[current_case]] = 1
        return result

    def get_vector_size(self):
        return len(self.case_to_position)

    def __repr__(self):
        return 'morphological case'
