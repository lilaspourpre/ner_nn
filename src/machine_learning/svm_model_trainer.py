# -*- coding: utf-8 -*-
import numpy as np
from sklearn import svm
from machine_learning.i_model_trainer import ModelTrainer
from enitites.models.svm_model import SvmModel
from sklearn import svm, model_selection


class SvmModelTrainer(ModelTrainer):
    def __init__(self, kernel=None):
        super().__init__()
        if kernel == 'linear':
            self.svm = svm.LinearSVC(C=1, class_weight=None, dual=True, fit_intercept=True,
                                     intercept_scaling=1, loss='squared_hinge', max_iter=1000,
                                     multi_class='ovr', penalty='l2', random_state=None, tol=0.0001,
                                     verbose=0)
        else:
            self.svm = svm.SVC(C=10, cache_size=200, class_weight=None, coef0=0.0,
                               decision_function_shape='ovr', degree=3, gamma='auto', kernel='rbf',
                               max_iter=-1, probability=False, random_state=None, shrinking=True,
                               tol=0.001, verbose=False)

    def train(self, tagged_vectors):
        # print(tagged_vectors)
        array_of_vectors = np.array([tagged_vector.get_vector() for tagged_vector in tagged_vectors])
        array_of_tags = np.array([tagged_vector.get_tag() for tagged_vector in tagged_vectors])
        self.svm.fit(array_of_vectors, array_of_tags)
        return SvmModel(self.svm)
