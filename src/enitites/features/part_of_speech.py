# -*- coding: utf-8 -*-
from enitites.features.morpho_feature import MorphoFeature


class POSFeature(MorphoFeature):
    TAGS = ('NOUN', 'VERB', 'ADJ', 'PREP', 'PNCT', 'CONJ')

    def __init__(self, pos_tags=TAGS):
        super().__init__('part of speech', pos_tags, predicate=self.__select_pos)

    @staticmethod
    def __select_pos(parsed_word):
        return parsed_word.tag.POS
