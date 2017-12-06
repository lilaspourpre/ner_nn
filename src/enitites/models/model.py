# -*- coding: utf-8 -*-
from abc import abstractmethod


class Model:
    def __init__(self):
        pass

    @abstractmethod
    def predict(self, vector):
        """
        :param vector: getting 1 vetor
        :return: tag for the vector
        """
        pass

    @abstractmethod
    def get_prefixes(self):
        pass

    @abstractmethod
    def get_suffixes(self):
        pass
