# -*- coding: utf-8 -*-
from enitites.features.check_in_list_feature import CheckInListFeature

class PunctFeature(CheckInListFeature):
    SIGNS = (',', '.', '?', '!', ':', '-', '—', '«', '»')

    def __init__(self, punct=SIGNS):
        super().__init__('punctuation', punct)