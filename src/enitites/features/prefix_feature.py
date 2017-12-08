# -*- coding: utf-8 -*-
from enitites.features.check_element_feature import CheckElementFeature


class PrefixFeature(CheckElementFeature):
    def __init__(self, prefixes, length):
        super().__init__('prefix', prefixes, lambda x: [x[:i] for i in range(1, length+1)])
