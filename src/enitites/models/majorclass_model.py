# -*- coding: utf-8 -*-
from src.enitites.models.model import Model
from src.enitites.tagged_vector import TaggedVector


class MajorClassModel(Model):
    def __init__(self, major_class):
        super().__init__()
        self.major_class = major_class

    def predict(self, list_of_vectors):
        tagged_vectors = []
        for vector in list_of_vectors:
            tagged_vectors.append(TaggedVector(vector=vector, tag=self.major_class))
        return tagged_vectors