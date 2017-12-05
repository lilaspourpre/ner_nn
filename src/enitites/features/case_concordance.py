# -*- coding: utf-8 -*-
import pymorphy2
from enitites.features.abstract_feature import AbstractFeature


class ConcordCaseFeature(AbstractFeature):
    """
    I'm not sure whether we should do it in Context feature
    """
    CASES = ('nomn', 'gent', 'datv', 'accs', 'ablt', 'loct', 'voct', 'gen2', 'acc2', 'loc2')

    def __init__(self, cases_to_detect=CASES):
        super().__init__()
        self.morph = pymorphy2.MorphAnalyzer() # XXX why pymorphy2 is still here?
        self.case_to_position = {}
        for position in range(len(cases_to_detect)):
            self.case_to_position[cases_to_detect[position]] = position

    def compute_vector_for(self, token, document):
        tokenlist = document.get_tokens()
        parsed_word = self.morph.parse(token.get_text())[0]
        current_case = str(parsed_word.tag.case)
        if current_case == None:
            return [0, 0]
        else:
            index = tokenlist.index(token) # XXX this looks like document method (and it can be made efficient!)
            return [self.__concord_to_the_left(current_case, index, tokenlist), self.__concord_to_the_right(current_case,
                                                                                                           index,
                                                                                                           tokenlist)]
    # XXX two methods below are copy/paste 
    def __concord_to_the_left(self, current_case, index, tokenlist):
        if index - 1 >= 0:
            return self.__compare_cases(current_case, index - 1, tokenlist)
        else:
            return 0

    def __concord_to_the_right(self, current_case, index, tokenlist):
        if index + 1 < len(tokenlist) - 1:
            return self.__compare_cases(current_case, index + 1, tokenlist)
        else:
            return 0

    def __compare_cases(self, current_case, other_index, tokenlist):
        parsed_word = self.morph.parse(tokenlist[other_index].get_text())[0]
        new_case = str(parsed_word.tag.case)
        if new_case == None:
            return 0
        else:
            return int(current_case == new_case)

    def get_vector_size(self):
        return 2

    def __repr__(self):
        return 'morphological case'
