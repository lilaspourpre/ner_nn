# -*- coding: utf-8 -*-
from enitites.features.check_element_feature import CheckElementFeature


class PrefixFeature(CheckElementFeature):
    def __init__(self, prefixes): # XXX i'd prefer having a parameter instead of hardcoded 3
        super().__init__('prefix', prefixes, lambda x: x[:3])
