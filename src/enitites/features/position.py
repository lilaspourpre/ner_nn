# -*- coding: utf-8 -*-
from src.enitites.features.abstract_feature import AbstractFeature

# XXX this feature seems to be a bad (useless) idea
class PositionFeature(AbstractFeature):
    def __init__(self):
        super().__init__()

    def compute_vector_for(self, token, document):
        return [int(token.get_position())]

    def __repr__(self):
        return 'position'
