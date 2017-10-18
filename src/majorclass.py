# -*- coding: utf-8 -*-
import codecs
import logging
import random


class MajorClass():
    def __init__(self):
        self.g = []
        self.dic_of_cands = {}
        self.sum_cand = 0

    def find_probabilities(self, list_of_cands):
        for cand in list_of_cands:
            if cand in self.dic_of_cands.keys():
                self.dic_of_cands[cand]+=1
            else:
                self.dic_of_cands[cand] = 1
        self.sum_cand = sum(self.dic_of_cands.values())

        prev = 0
        counter = 0
        for i in self.dic_of_cands:
            curr = self.dic_of_cands[i]
            if counter == 0:
                self.dic_of_cands[i] = [-0.1, prev + round(self.dic_of_cands[i] / self.sum_cand, 20)]
            elif counter == len(self.dic_of_cands) - 1:
                self.dic_of_cands[i] = [prev, 1]
            else:
                self.dic_of_cands[i] = [prev, prev + round(self.dic_of_cands[i] / self.sum_cand, 20)]
            prev += round(curr / self.sum_cand,20)
            counter += 1

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

    def fit(self, corpus, type_of_algorythm):
        self.type_of_algorythm = type_of_algorythm
        data = []
        tags = []
        for row in corpus:
            data.append(row[:2])
            tags.append(row[3])
        if type_of_algorythm == 'majorclass':
            self.checkMajority(tags)
        elif type_of_algorythm == 'random':
            self.find_probabilities(tags)
        else:
            logging.log(logging.ERROR, 'The type of algorytm you mentioned is not suitable')
            raise ValueError

    def predict(self, data):
        dic_of_tag_for_each_file = {}
        if self.type_of_algorythm == 'majorclass':
            for file in data.keys():
                tags = {}
                for i in data[file]:
                    tags[i] = self.majority_class
                dic_of_tag_for_each_file[file] = tags
        elif self.type_of_algorythm == 'random':
            for file in data.keys():
                tags = {}
                for token in data[file]:
                    random_number = random.uniform(0, 1) # gives random number from 0 to 1
                    for key in self.dic_of_cands:
                        if random_number>self.dic_of_cands[key][0] and random_number<=self.dic_of_cands[key][1]:
                            tags[token]= key
                            break
                dic_of_tag_for_each_file[file]= tags
        else:
            logging.log(logging.ERROR, 'The type of algorytm you mentioned is not suitable')
            raise ValueError
        return dic_of_tag_for_each_file
