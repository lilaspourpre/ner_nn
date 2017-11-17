# -*- coding: utf-8 -*-
from abc import abstractmethod


class AbstractFeature():
    def __init__(self):
        pass

    @abstractmethod
    def compute_vector_for(self, token, tokenslist):
        """
        :param token: tokenObject
        :param tokenslist: list of all document tokens
        :return: vector
        """
        pass

    @abstractmethod
    def get_vector_size(self):
        pass
