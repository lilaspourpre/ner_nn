# -*- coding: utf-8 -*-
from src.enitites.features.case import CaseFeature

# XXX use composition instead of Inheritance
class NextCaseFeature(CaseFeature):
    def __init__(self):
        super().__init__()

    def compute_vector_for(self, token, document):
        current_index = document.index(token)
        if current_index != len(document) - 1:
            next_token = document[current_index + 1]
            return self._count_case_vector(next_token)
        else:
            return [1, 0, 0]

    def __repr__(self):
        return 'next_case'
