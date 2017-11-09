# -*- coding: utf-8 -*-
from abc import abstractmethod

class Model():
    def __init__(self):
        pass

    @abstractmethod
    def predict(self, vectors):
        pass