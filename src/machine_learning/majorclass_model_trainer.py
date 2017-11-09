# -*- coding: utf-8 -*-
import logging
from collections import Counter
from src.machine_learning.i_model_trainer import ModelTrainer
from src.enitites.models.majorclass_model import MajorClassModel


class MajorClassModelTrainer(ModelTrainer):
    def __init__(self):
        super().__init__()

    # Function to check if the candidate occurs more than n/2 times
    def __is_major(self, length, candidate_count):
        if candidate_count > length / 2:
            return True
        else:
            return False

    # Function to print Majority Element
    def __find_majority_class(self, list_of_candidates):
        counted_tags = Counter(list_of_candidates)
        candidate_tag, candidate_count = counted_tags.most_common(1)[0]
        if self.__is_major(len(list_of_candidates), candidate_count):
            logging.log(logging.INFO, 'major_class = ' + str(candidate_tag))
            return candidate_tag
        else:
            raise Exception

    def train(self, tagged_vectors):
        tags = [tagged_vector.get_tag() for tagged_vector in tagged_vectors]
        major_class = self.__find_majority_class(tags)
        return MajorClassModel(major_class)
