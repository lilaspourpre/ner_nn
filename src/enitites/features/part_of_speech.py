# -*- coding: utf-8 -*-
from enitites.features.check_in_list_feature import CheckInListFeature

class POSFeature(CheckInListFeature):
    TAGS = ('NOUN', 'VERB', 'ADJ', 'PREP', 'PNCT', 'CONJ')

    def __init__(self, pos_tags=TAGS):
        super().__init__('part of speech', pos_tags, function=".tag.POS")
