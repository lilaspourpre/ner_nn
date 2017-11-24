# -*- coding: utf-8 -*-
from src.enitites.features.abstract_feature import AbstractFeature

class NumbersInTokenFeature(AbstractFeature):
    def __init__(self):
        super().__init__()
        self.predicates = [str.isalpha, str.isdigit, str.isalnum]

    def compute_vector_for(self, token, tokenlist):
        result = []
        for predicate in self.predicates:
            result.append(int(predicate(token.get_text())))
        return result

    def get_vector_size(self):
        return len(self.predicates)

    def __repr__(self):
        return 'numbers_in_token'
