# -*- coding: utf-8 -*-
from enitites.features.abstract_feature import AbstractFeature


class CheckInListFeature(AbstractFeature):
    def __init__(self, name, list_of_strings, function=None, return_type=1):
        """
        :param name:
        :param list_of_strings:
        :param return_type: normal=1 or reverse=0 (0 instead of 1)
        :param function:
        """
        super().__init__()
        self.name = name
        self.return_type = return_type
        self.function = function
        self.strings_with_position = {}
        for position in range(len(list_of_strings)):
            self.strings_with_position[list_of_strings[position]] = position

    def compute_vector_for(self, token, document):
        result = [0] * self.get_vector_size()
        if self.function:
            parsed_words = document.get_morpho_parsed_tokens()
            parsed_word = parsed_words[token.get_id()]
            what_to_compare = str(eval("parsed_word" + self.function))
        else:
            what_to_compare = token.get_text()
        if what_to_compare in self.strings_with_position:
            result[self.strings_with_position[what_to_compare]] = 1
        return self.__check(result)

    def __check(self, result):
        if self.return_type == 0:
            return [int(i == 0) for i in result]
        else:
            return result

    def get_vector_size(self):
        return len(self.strings_with_position)

    def __repr__(self):
        return self.name
