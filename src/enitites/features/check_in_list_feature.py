# -*- coding: utf-8 -*-
from enitites.features.abstract_feature import AbstractFeature


class CheckInListFeature(AbstractFeature):
    def __init__(self, name, set_of_strings, forward=True):
        """
        :param name:
        :param set_of_strings:
        :param forward:
        """
        super().__init__()
        self.name = name
        self.forward = forward
        self.strings_with_position = set(set_of_strings) # XXX why with_position?

    def compute_vector_for(self, token, document):
        text_token = token.get_text()
        return self.__check(text_token in self.strings_with_position)

    def __check(self, result):
        return [int(self.forward == result)]

    def get_vector_size(self):
        return len(self.strings_with_position)

    def __repr__(self):
        return self.name
