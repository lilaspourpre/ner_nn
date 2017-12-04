# -*- coding: utf-8 -*-
import bisect
from collections import Counter
from enitites.features.abstract_feature import AbstractFeature


class DFFeature(AbstractFeature):
    def __init__(self):
        super().__init__()

    def compute_vector_for(self, token, document):
        words_counts = Counter([t.get_text() for t in document.get_tokens()])
        return [words_counts[token.get_text()]]

    def get_vector_size(self):
        return 1

    def __repr__(self):
        return 'doc_frequency'