# -*- coding: utf-8 -*-
from src.enitites.features.abstract_feature import AbstractFeature

class FeatureComposite(AbstractFeature):
    def __init__(self, feature_list=None): # XXX I'd rather used empty list as default
        super().__init__()
        self.feature_list = feature_list

    def compute_vector_for(self, token, document):
        final_vector = []
        for feature in self.feature_list:
            final_vector.extend(feature.compute_vector_for(token, document))
        return final_vector

    def __repr__(self):
        return "<<" + ', '.join([repr(i) for i in self.feature_list]) + ">>"

    # XXX excess method
    def get_feature_list_length(self):
        # XXX fails when feature_list is None (default value)
        return len(self.feature_list)
