# -*- coding: utf-8 -*-
import logging
from collections import Counter
from src.machine_learning.i_model_trainer import ModelTrainer
from src.enitites.models.majorclass_model import MajorClassModel


class MajorClassModelTrainer(ModelTrainer):
    def __init__(self):
        super().__init__()

    def __is_major(self, length, candidate_count):
        """
        Function to check if the candidate occurs more than n/2 times
        :param length: length of tokenlist
        :param candidate_count: how many times does the candidate occurs
        :return: True if is the majority class else if not
        """
        return candidate_count > length / 2

    def __find_majority_class(self, list_of_candidates):
        """
        :param list_of_candidates:
        :return:
        """
        counted_tags = Counter(list_of_candidates)
        candidate_tag, candidate_count = counted_tags.most_common(1)[0]
        # XXX strange logic with "candidate occurs more than n/2 times"
        # YYY: why?
        # ZZZ: from my point of view, major tag is just the most frequent tag.
        # From your point of view, it is the tag, which appears in more than half of instances.
        # My interpretation seems to be OK, when we have, for example, 3 tags which appear
        # in 40%, 30% and 30% of instances.
        # Your interpretation seems to fail with Exception
        if self.__is_major(len(list_of_candidates), candidate_count):
            logging.log(logging.INFO, 'major_class = ' + str(candidate_tag))
            return candidate_tag
        else:
            raise Exception

    def train(self, tagged_vectors):
        tags = [tagged_vector.get_tag() for tagged_vector in tagged_vectors]
        major_class = self.__find_majority_class(tags)
        return MajorClassModel(major_class)
