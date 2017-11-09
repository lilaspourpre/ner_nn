# -*- coding: utf-8 -*-
from abc import abstractmethod

class ModelTrainer():
    def __init__(self):
        pass

    @abstractmethod
    def train(self, tagged_vectors):
        pass
