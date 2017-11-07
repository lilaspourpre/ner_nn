# -*- coding: utf-8 -*-

class TaggedToken:
    def __init__(self, tag, token):
        self.__tag = tag
        self.__token = token

    def get_token(self):
        return self.__token

    def get_tag(self):
        return self.__tag
    
    def __repr__(self):
        return "<" + self.__tag + "_" + str(self.__token) + ">"
