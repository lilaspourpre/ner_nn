# -*- coding: utf-8 -*-
import texterra
#t = texterra.API('YOURKEY')
import pymorphy2
morph = pymorphy2.MorphAnalyzer()
from src.enitites.features.part_of_speech import POSFeature

# XXX duplicates NextPOSFeature, PrevCaseFeature, PrevMorphoCaseFeature
class PrevPOSFeature(POSFeature):
    def __init__(self):
        super().__init__()

    def compute_vector_for(self, token, document):
        current_index = document.index(token)
        if current_index != len(document) - 1: # XXX obvious reason, why NOT to copy-paste code
            prev_token = document[current_index + 1]
            return self._count_pos_vector(prev_token)
        else:
            return [1, 1, 1]

    def __repr__(self):
        return 'previous part of speech'
