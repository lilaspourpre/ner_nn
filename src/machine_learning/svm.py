# -*- coding: utf-8 -*-
from sklearn import svm
import numpy as np
from  src.machine_learning.abstract_method import AbsractMethod
import src.machine_learning.features as features


class NerSvm(AbsractMethod):
    def __init__(self, path=None, decision_function_shape='ovo', kernel=None):
        super().__init__()
        self.feature_class = features.FeatureMaking(path)
        if kernel == 'linear':
            self.svm = svm.LinearSVC()
        else:
            self.svm = svm.SVC(decision_function_shape=decision_function_shape)

    def fit(self, corpus):
        array_of_vectors = np.array([self.feature_class.create_features(word) for word in corpus])
        tags = np.array([word[3] for word in corpus])
        self.svm.fit(array_of_vectors, tags)

    def predict(self, testset_tokens):
        dic_of_tags_for_each_file = {}
        vectors = self.features(testset_tokens)
        for file in vectors.keys():
            print(vectors[file])
            words = [i[0] for i in vectors[file]]
            tags = self.svm.predict([i[1] for i in vectors[file]])
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
