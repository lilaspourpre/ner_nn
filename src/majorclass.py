# -*- coding: utf-8 -*-
import codecs
import logging

class MajorClass():
    def __init__(self):
        self.g = []

    def findCandidate(self, list_of_cands):
        candidate = 0
        count = 0
        for i in list_of_cands:
            if count == 0:
                candidate = i
            if i == candidate:
                count += 1
            else:
                count -= 1
        return candidate

    # Function to check if the candidate occurs more than n/2 times
    def isMajority(self, list_of_cands, cand):
        count = 0
        for i in list_of_cands:
            if i == cand:
                count += 1
        if count > len(list_of_cands) / 2:
            return True
        else:
            return False

    # Function to print Majority Element
    def checkMajority(self, list_of_cands):
        cand = self.findCandidate(list_of_cands)
        if self.isMajority(list_of_cands, cand):
            self.majority_class = cand
            logging.log(logging.INFO, 'major_class = '+str(cand))
        else:
            raise Exception

    def fit(self, corpus):
        data = []
        tags = []
        for row in corpus:
            data.append(row[:2])
            tags.append(row[3])
        self.checkMajority(tags)

    def predict(self, data):
        tags = [self.majority_class for i in data]
        return tags
