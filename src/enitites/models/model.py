# -*- coding: utf-8 -*-
from abc import abstractmethod

class Model():
    def __init__(self):
        pass

    # XXX vectors or vector? major takes list of vectors, but returns single tag
    # XXX random and svm take on vector, return tag
    @abstractmethod
    def predict(self, vectors):
        pass