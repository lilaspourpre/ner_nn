# -*- coding: utf-8 -*-
import numpy as np
from enitites.models.model import Model


class SvmModel(Model):
    def __init__(self, svm, prefixes, suffixes):
        super().__init__()
        self.svm = svm
        self.__prefixes = prefixes
        self.__suffixes = suffixes

    def predict(self, vector):
        array_of_vectors = np.array([vector])
        return self.svm.predict(array_of_vectors)[0]

    def __repr__(self):
        return 'svm_model'

    def get_prefixes(self):
        return self.__prefixes

    def get_suffixes(self):
        return self.__suffixes




