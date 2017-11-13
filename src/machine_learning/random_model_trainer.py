# -*- coding: utf-8 -*-
import logging
from collections import Counter
from src.machine_learning.i_model_trainer import ModelTrainer
from src.enitites.models.random_model import RandomModel


class RandomModelTrainer(ModelTrainer):
    def __init__(self):
        super().__init__()

    def __find_probabilities(self, list_of_candidates):
        """
        :param list_of_candidates:
        :return:
        """
        NUMBER_OF_SYMBOLS_AFTER_COMMA = 10
        dict_of_candidates_with_counted_tags = Counter(list_of_candidates)
        quantity_of_all_tags = len(list_of_candidates)
        prev = 0
        counter = 0
        dict_of_distributed_probabilities = {}

        # XXX consider using dict_of_candidates_with_counted_tags.items()
        for candidate in dict_of_candidates_with_counted_tags:
            current_counted_tags = dict_of_candidates_with_counted_tags[candidate]
            # XXX what's the use of round here?
            current_weight = round(current_counted_tags / quantity_of_all_tags, NUMBER_OF_SYMBOLS_AFTER_COMMA)
            if counter == 0:
                dict_of_distributed_probabilities[candidate] = [-0.1, current_weight]
            elif counter == len(dict_of_candidates_with_counted_tags) - 1:
                dict_of_distributed_probabilities[candidate] = [prev, 1]
            else:
                dict_of_distributed_probabilities[candidate] = [prev, prev + current_weight]
            prev += current_weight
            counter += 1
        return dict_of_distributed_probabilities

    def train(self, tagged_vectors):
        tags = [tagged_vector.get_tag() for tagged_vector in tagged_vectors]
        dict_of_distributed_probabilities = self.__find_probabilities(tags)
        logging.log(logging.INFO, dict_of_distributed_probabilities)
        return RandomModel(dict_of_distributed_probabilities)
