# -*- coding: utf-8 -*-
from enitites.features.abstract_feature import AbstractFeature
from enitites.features.check_in_list_feature import CheckInListFeature
from enitites.token import Token


class LowerCaseFeature(AbstractFeature):
    def __init__(self):
        super().__init__()

    # XXX overcomplicated
    def compute_vector_for(self, token, document):
        token_text = token.get_text().lower()
        if token_text != token.get_text():
            list_of_words = tuple(set([t.get_text() for t in document.get_tokens()]))
            check_lower = CheckInListFeature('lowercase', list_of_words)
            low_token = Token(tokenid=token.get_id(), position=token.get_position(), length=token.get_length(),
                                      text=token_text)
            vector = check_lower.compute_vector_for(low_token, document)
            return [0] if 1 in vector else [1]
        else:
            return [0]

    def get_vector_size(self):
        return 1

    def __repr__(self):
        return 'lowercase'
