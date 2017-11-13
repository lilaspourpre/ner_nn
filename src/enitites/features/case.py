# -*- coding: utf-8 -*-
from src.enitites.features.abstract_feature import AbstractFeature

class CaseFeature(AbstractFeature):
    def __init__(self):
        super().__init__()

    def compute_vector_for(self, token, document):
        return self._count_case_vector(token)

    def _count_case_vector(self, token):
        # XXX bad idea of encoding
        if token.get_text().isupper():
            return [0, 0, 0]
        elif token.get_text().islower():
            return [0, 0, 1]
        elif token.get_text().istitle():
            return [0, 1, 0]
        else:
            return [0, 1, 1]

    def __repr__(self):
        return 'case'
