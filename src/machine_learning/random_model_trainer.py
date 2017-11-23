# -*- coding: utf-8 -*-
import logging
from collections import Counter
from sortedcontainers import SortedDict
from src.machine_learning.i_model_trainer import ModelTrainer
from src.enitites.models.random_model import RandomModel


class RandomModelTrainer(ModelTrainer):
    def __init__(self):
        super().__init__()

    def __find_probabilities(self, list_of_candidates):
        """
        :param list_of_candidates:
        :return: dict_of_distributed_probabilities
        """
        dict_of_candidates_with_counted_tags = Counter(list_of_candidates)
        prev_weight = 0
        counter = 0
        dict_of_distributed_probabilities = SortedDict()

        for tag, current_count in dict_of_candidates_with_counted_tags.items():
            current_weight = current_count / len(list_of_candidates)
            if counter == 0:
                dict_of_distributed_probabilities[current_weight] = tag
            elif counter == len(dict_of_candidates_with_counted_tags) - 1:
                dict_of_distributed_probabilities[1] = tag
            else:
                dict_of_distributed_probabilities[prev_weight + current_weight] = tag
            prev_weight += current_weight
            counter += 1
        print(dict_of_distributed_probabilities)
        return dict_of_distributed_probabilities

    def train(self, tagged_vectors):
        tags = [tagged_vector.get_tag() for tagged_vector in tagged_vectors]
        dict_of_distributed_probabilities = self.__find_probabilities(tags)
        logging.log(logging.INFO, dict_of_distributed_probabilities)
        return RandomModel(dict_of_distributed_probabilities)
