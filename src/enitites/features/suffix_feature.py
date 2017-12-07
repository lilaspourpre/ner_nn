# -*- coding: utf-8 -*-
from enitites.features.check_element_feature import CheckElementFeature


class SuffixFeature(CheckElementFeature):
    def __init__(self, suffixes):
        super().__init__('suffix', suffixes, lambda x: x[-3:])
