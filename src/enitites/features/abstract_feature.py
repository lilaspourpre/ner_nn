# -*- coding: utf-8 -*-
from abc import abstractmethod, ABCMeta

# XXX what is ABCMeta for?
class AbstractFeature(metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def compute_vector_for(self, token, document):
        """
        :param token: tokenObject
        XXX and what is document?
        :return: vector
        """
        pass
