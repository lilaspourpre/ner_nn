#-*- coding: utf-8 -*-
from src.enitites.features.abstract_feature import AbstractFeature

class LengthFeature(AbstractFeature):
    def __init__(self):
        super().__init__()

    def compute_vector_for(self, token, document):
        return [len(token.get_text())]

    def __repr__(self):
        return 'length'

