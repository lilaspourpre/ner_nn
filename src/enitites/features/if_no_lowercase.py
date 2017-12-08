# -*- coding: utf-8 -*-
from enitites.features.abstract_feature import AbstractFeature


class LowerCaseFeature(AbstractFeature):
    def __init__(self):
        super().__init__()

    # XXX this feature looks interesting, but I'd invert it: 1 if this word is somewhere in document in lowercase
    def compute_vector_for(self, token, document):
        token_text_low = token.get_text().lower()
        if token_text_low != token.get_text(): # XXX this check is excess
            set_of_words = set(document.get_token_texts())
            return [0] if token_text_low in set_of_words else [1]
        else:
            return [0]

    def get_vector_size(self):
        return 1

    def __repr__(self):
        return 'lowercase'
