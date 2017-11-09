# -*- coding: utf-8 -*-
from src.enitites.models.model import Model


class MajorClassModel(Model):
    def __init__(self, major_class):
        super().__init__()
        self.major_class = major_class

    def predict(self, list_of_vectors):
        return self.major_class