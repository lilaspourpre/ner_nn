# -*- coding: utf-8 -*-

class TaggedTokens:
    def __init__(self, tag=None, token=None):
        self.__tag = tag
        self.__token = token

    def get_token(self):
        return self.__token

    def get_tag(self):
        return self.__tag

    def set_tag(self, tag):
        self.__tag = tag

    def set_token(self, token):
        self.__token = token
