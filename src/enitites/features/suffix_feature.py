# -*- coding: utf-8 -*-
from enitites.features.check_element_feature import CheckElementFeature


class SuffixFeature(CheckElementFeature):
    def __init__(self, suffixes, length):
        super().__init__('suffix', suffixes, lambda x: [x[i:] for i in range(-length, 0)])
