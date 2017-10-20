# -*- coding: utf-8 -*-
from sklearn import svm
import numpy as np

import src.machine_learning.features as features


class NerSvm:
    def __init__(self, decision_function_shape='ovo', kernel=None):
        self.feature_class = features.FeatureMaking()
        if kernel == 'linear':
            self.svm = svm.LinearSVC()
        else:
            self.svm = svm.SVC(decision_function_shape=decision_function_shape)

    def fit(self, corpus):
        x = np.array([self.feature_class.create_features(word) for word in corpus])
        self.x = x
        y = np.array([word[3] for word in corpus])
        self.svm.fit(x, y)

    def predict(self, testset_tokens):
        dic_of_tags_for_each_file = {}
        dec = self.svm.decision_function(self.x)
        print(dec.shape[1], "shape")
        vectors = self.features(testset_tokens)
        for file in vectors.keys():
            words = [i[0] for i in vectors[file]]
            tags = self.svm.predict([i[1:] for i in vectors[file]])
            for i in range(len(words)):
                dic_of_tags_for_each_file[words[i]] = tags[i]
        return dic_of_tags_for_each_file

    def features(self, tokens):
        dic_of_vectors_for_each_file = {}
        for file in tokens.keys():
            features = []
            for word in tokens[file].keys():
                features.append(word)
                features.append(self.feature_class.create_features(tokens[file][word]))
            dic_of_vectors_for_each_file[file] = features
        return dic_of_vectors_for_each_file
