# -*- coding: utf-8 -*-

class FeatureMaking:
    def __init__(self):
        self.list_of_features = []
        self.token_id =None
        self.token_text = None
        self.position = None

    def create_features(self, word):
        print(word)
        self.token_id = word[0]
        self.token_text = word[1]
        self.position = word[2]
        self.length()
        return self.list_of_features

    def length(self):
        pass

    def pos(self):
        pass
