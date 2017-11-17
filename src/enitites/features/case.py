# -*- coding: utf-8 -*-
from src.enitites.features.abstract_feature import AbstractFeature

class CaseFeature(AbstractFeature):
    def __init__(self):
        super().__init__()
        self.predicates = [str.isupper, str.islower, str.istitle]

    def compute_vector_for(self, token, tokenlist):
        return self._count_case_vector(token)

    def _count_case_vector(self, token):
        result = []
        for predicate in self.predicates:
            result.append(int(predicate(token.get_text())))
        return result

    def get_vector_size(self):
        return len(self.predicates)

    def __repr__(self):
        return 'case'
