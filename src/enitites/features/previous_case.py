# -*- coding: utf-8 -*-
from src.enitites.features.case import CaseFeature


class PrevCaseFeature(CaseFeature):
    def __init__(self):
        super().__init__()

    def compute_vector_for(self, token, document):
        current_index = document.index(token)
        if current_index != 0:
            prev_token = document[current_index - 1]
            return self._count_case_vector(prev_token)
        else:
            return [1, 0, 0]

    def __repr__(self):
        return 'prev_case'
