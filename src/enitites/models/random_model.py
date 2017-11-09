# -*- coding: utf-8 -*-
import random
from src.enitites.models.model import Model
from src.enitites.tagged_vector import TaggedVector


class RandomModel(Model):
    def __init__(self, dict_of_distributed_probabilities):
        super().__init__()
        self.dict_of_distributed_probabilities = dict_of_distributed_probabilities

    def predict(self, list_of_vectors):
        tagged_vectors = []
        for vector in list_of_vectors:
            random_number = random.uniform(0, 1)  # gives random number from 0 to 1
            for tag in self.dict_of_distributed_probabilities:
                if self.dict_of_distributed_probabilities[tag][0] < random_number \
                        <= self.dict_of_distributed_probabilities[tag][1]:
                    tagged_vectors.append(TaggedVector(vector=vector, tag=tag))
                    break
        return tagged_vectors