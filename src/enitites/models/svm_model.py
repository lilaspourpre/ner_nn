# -*- coding: utf-8 -*-
import numpy as np
from src.enitites.models.model import Model
from src.enitites.tagged_vector import TaggedVector

class SvmModel(Model):
    def __init__(self, svm):
        super().__init__()
        self.svm = svm

    def predict(self, list_of_vectors):
        tagged_vectors = []
        for vector in list_of_vectors:
            array_of_vectors = np.array([vector.get_vector()])
            tag = self.svm.predict(array_of_vectors)[0]
            tagged_vectors.append(TaggedVector(vector=vector, tag=tag))
        return tagged_vectors