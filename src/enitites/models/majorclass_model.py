# -*- coding: utf-8 -*-
from enitites.models.model import Model


class MajorClassModel(Model):
    def __init__(self, major_class, prefixes, suffixes):
        super().__init__()
        self.major_class = major_class
        self.__prefixes = prefixes
        self.__suffixes = suffixes

    def predict(self, vector):
        return self.major_class

    def __repr__(self):
        return 'majorclass_model'

    def get_prefixes(self):
        return self.__prefixes

    def get_suffixes(self):
        return self.__suffixes
