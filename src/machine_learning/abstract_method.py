# -*- coding: utf-8 -*-
from abc import abstractmethod


class AbsractMethod:
    def __init__(self):
        pass

    @abstractmethod
    def fit(self, corpus):
        pass

    @abstractmethod
    def predict(self, data):
        pass
