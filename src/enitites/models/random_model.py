# -*- coding: utf-8 -*-
import random
from src.enitites.models.model import Model


class RandomModel(Model):
    def __init__(self, dict_of_distributed_probabilities):
        super().__init__()
        self.dict_of_distributed_probabilities = dict_of_distributed_probabilities

    def predict(self, vector):
        random_number = random.uniform(0, 1)  # gives random number from 0 to 1
        for tag in self.dict_of_distributed_probabilities:
            if self.dict_of_distributed_probabilities[tag][0] < random_number \
                    <= self.dict_of_distributed_probabilities[tag][1]:
                return tag