# -*- coding: utf-8 -*-
from src.enitites.features.predicate_feature import PredicateFeature

class NumbersInTokenFeature(PredicateFeature):
    def __init__(self, predicates=(str.isalpha, str.isdigit, str.isalnum)):
        super().__init__('numbers_in_token', predicates)