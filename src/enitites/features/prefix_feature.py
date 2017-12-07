# -*- coding: utf-8 -*-
from enitites.features.check_element_feature import CheckElementFeature


class PrefixFeature(CheckElementFeature):
    def __init__(self, prefixes):
        super().__init__('prefix', prefixes, lambda x: x[:3])
