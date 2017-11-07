# -*- coding: utf-8 -*-


class Document:
    def __init__(self, list_of_tagged_tokens):
        self.__list_of_tagged_tokens = list_of_tagged_tokens

    def get_tagged_tokens(self):
        return self.__list_of_tagged_tokens
