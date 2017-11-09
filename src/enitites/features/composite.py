# -*- coding: utf-8 -*-
from src.enitites.features.abstract_feature import AbstractFeature

class FeatureComposite(AbstractFeature):
    def __init__(self, feature_list):
        super().__init__()
        self.feature_list = feature_list

    def compute_vector_for(self, token):
        final_vector = []
        for feature in self.feature_list:
            #final_vector.extend(feature.compute_vector_for(token))
            final_vector.append(1)
        return final_vector
