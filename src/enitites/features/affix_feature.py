# -*- coding: utf-8 -*-
import itertools
from enitites.features.abstract_feature import AbstractFeature

# XXX Congratulations! You've successfully stepped on this rake!
class AffixFeature(AbstractFeature):
    def __init__(self, type_of_aff, affixes = None, length=3):
        super().__init__()
        self.strings_with_position = {}
        if affixes is None:
            affixes = self.__compute_affixes(length)
        for position in range(len(tuple(affixes))):
            self.strings_with_position[affixes[position]] = position
        if 'pre' in type_of_aff:
            self.aff_alg = "[0:3]"
        elif 'suf' in type_of_aff:
            self.aff_alg = "[-3:]"
        else:
            raise ValueError('type of affixes should contain "pre" (for prefix) or "suf" (for suffix)')

    def __compute_affixes(self, length):
        affixes = set()
        list_of_combs = list(itertools.combinations_with_replacement([chr(i) for i in range(1072, 1104)], length))
        for comb in list_of_combs:
            for i in list(itertools.permutations(comb)):
                affixes.update([''.join(i)])
        return tuple(affixes)

    def compute_vector_for(self, token, document):
        result = [0] * self.get_vector_size()
        text_token = token.get_text()
        cur_aff = eval('text_token'+self.aff_alg).lower()
        if cur_aff in self.strings_with_position:
            result[self.strings_with_position[cur_aff]] = 1
        return result

    def get_vector_size(self):
        return len(self.strings_with_position)

    def __repr__(self):
        return 'affix_feature'