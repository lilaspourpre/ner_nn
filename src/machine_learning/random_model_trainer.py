# -*- coding: utf-8 -*-
import logging
from collections import Counter
from src.machine_learning.i_model_trainer import ModelTrainer
from src.enitites.models.random_model import RandomModel


class RandomModelTrainer(ModelTrainer):
    def __init__(self):
        super().__init__()
        self.NUMBER_OF_SYMBOLS_AFTER_COMMA = 10

    def __find_probabilities(self, list_of_candidates):
        """
        :param list_of_candidates:
        :return: dict_of_distributed_probabilities
        """
        dict_of_candidates_with_counted_tags = Counter(list_of_candidates)
        prev_weight = 0
        counter = 0
        dict_of_distributed_probabilities = {}

        for tag, current_count in dict_of_candidates_with_counted_tags.items():
            # XXX what's the use of round here?
            # YYY current weight for creating list with the range (two numbers), then we compare the randomly generated number with this range
            # ZZZ I understand the code. I just can't understand the invocation of round(...)
            # In other words, why can't i simply write:
            # current_weight = current_count / len(list_of_candidates)
            current_weight = round(current_count / len(list_of_candidates), self.NUMBER_OF_SYMBOLS_AFTER_COMMA)
            if counter == 0:
                dict_of_distributed_probabilities[tag] = [-0.1, current_weight]
            elif counter == len(dict_of_candidates_with_counted_tags) - 1:
                dict_of_distributed_probabilities[tag] = [prev_weight, 1]
            else:
                dict_of_distributed_probabilities[tag] = [prev_weight, prev_weight + current_weight]
            prev_weight += current_weight
            counter += 1
        return dict_of_distributed_probabilities

    def train(self, tagged_vectors):
        tags = [tagged_vector.get_tag() for tagged_vector in tagged_vectors]
        dict_of_distributed_probabilities = self.__find_probabilities(tags)
        logging.log(logging.INFO, dict_of_distributed_probabilities)
        return RandomModel(dict_of_distributed_probabilities)
