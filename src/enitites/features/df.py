# -*- coding: utf-8 -*-
from collections import Counter
from enitites.features.abstract_feature import AbstractFeature


class DFFeature(AbstractFeature):
    def __init__(self):
        super().__init__()

    def compute_vector_for(self, token, document):
        words_counts = Counter(document.get_token_texts()) # XXX still have to count tokens all the time. Why not store Counter within doc?
        return [words_counts[token.get_text()]] # XXX maybe normalize counts?

    def get_vector_size(self):
        return 1

    def __repr__(self):
        return 'doc_frequency'
