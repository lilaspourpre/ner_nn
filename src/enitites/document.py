# -*- coding: utf-8 -*-


class Document:
    def __init__(self, list_of_tagged_tokens):
        self.__list_of_tagged_tokens = list_of_tagged_tokens

    def get_tagged_tokens(self):
        return self.__list_of_tagged_tokens

    def get_tokens(self):
        document_list_with_tokens = []
        for tagged_token in self.get_tagged_tokens():
            document_list_with_tokens.append(tagged_token.get_token())
        return document_list_with_tokens

