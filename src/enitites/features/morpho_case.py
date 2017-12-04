# -*- coding: utf-8 -*-
from enitites.features.check_in_list_feature import CheckInListFeature


class MorphoFeature(CheckInListFeature):
    CASES = ('nomn', 'gent', 'datv', 'accs', 'ablt', 'loct', 'voct', 'gen2', 'acc2', 'loc2')

    def __init__(self, cases=CASES):
        super().__init__('morphological case', cases, function=".tag.case")