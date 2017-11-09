# -*- coding: utf-8 -*-


class TaggedVector():
    def __init__(self, tag, vector):
        self.__tag = tag
        self.__vector = vector

    def get_vector(self):
        return self.__vector

    def get_tag(self):
        return self.__tag

    def __repr__(self):
        return "<" + self.__tag + "_" + str(self.__vector) + ">"
