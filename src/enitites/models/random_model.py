# -*- coding: utf-8 -*-
import random
import copy
from src.enitites.models.model import Model


class RandomModel(Model):
    def __init__(self, dict_of_distributed_probabilities):
        super().__init__()
        self.dict_of_distributed_probabilities = dict_of_distributed_probabilities

    def predict(self, vector):
        random_number = random.uniform(0, 1)  # gives random number from 0 to 1
        new_dict = copy.deepcopy(self.dict_of_distributed_probabilities)
        new_dict[random_number] = None
        new_index = new_dict.index(random_number)
        key = self.dict_of_distributed_probabilities.iloc[new_index]
        return self.dict_of_distributed_probabilities[key]


    def __repr__(self):
        return 'random_model'

