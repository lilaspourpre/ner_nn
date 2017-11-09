# -*- coding: utf-8 -*-
from abc import abstractmethod, ABCMeta


class AbstractFeature(metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def compute_vector_for(self, token):
        """
        :param token: tokenObject
        :return: vector
        """
        pass
