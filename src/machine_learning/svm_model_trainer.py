# -*- coding: utf-8 -*-
import numpy as np
import logging
from sklearn import svm
from src.machine_learning.i_model_trainer import ModelTrainer
from src.enitites.models.svm_model import SvmModel


class SvmModelTrainer(ModelTrainer):
    def __init__(self, decision_function_shape='ovo', kernel=None):
        super().__init__()
        if kernel == 'linear':
            self.svm = svm.LinearSVC()
        else:
            self.svm = svm.SVC(decision_function_shape=decision_function_shape)

    def train(self, tagged_vectors):
        logging.log(logging.INFO, tagged_vectors)
        array_of_vectors = np.array([tagged_vector.get_vector() for tagged_vector in tagged_vectors])
        array_of_tags = np.array([tagged_vector.get_tag() for tagged_vector in tagged_vectors])
        self.svm.fit(array_of_vectors, array_of_tags)
        return SvmModel(self.svm)