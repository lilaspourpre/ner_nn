# -*- coding: utf-8 -*-
import re
from enitites.features.predicate_feature import PredicateFeature


class LettersFeature(PredicateFeature):
    def __init__(self, reg_exps=(u'[a-zA-Z]+', u'[а-яА-Я]+')):
        predicates = [self.__create_search_predicate(reg) for reg in reg_exps]
        super().__init__(name='letters_type', list_of_predicates=predicates)

    def __create_search_predicate(self, reg):
        return lambda x: 0 if re.compile(reg).search(x) == None else 1 # XXX compiling regexp each time is a bad idea
