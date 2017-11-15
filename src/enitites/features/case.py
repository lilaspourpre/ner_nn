# -*- coding: utf-8 -*-
from src.enitites.features.abstract_feature import AbstractFeature

class CaseFeature(AbstractFeature):
    def __init__(self):
        super().__init__()

    def compute_vector_for(self, token, tokenlist):
        return self._count_case_vector(token)

    def _count_case_vector(self, token):
        result = []
        result.append(1) if token.get_text().isupper() else result.append(0)
        result.append(1) if token.get_text().islower() else result.append(0)
        result.append(1) if token.get_text().istitle() else result.append(0)
        return result

    def get_vector_size(self):
        return 3

    def __repr__(self):
        return 'case'
