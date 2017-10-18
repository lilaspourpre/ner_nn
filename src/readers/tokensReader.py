# -*- coding: utf-8 -*-
import random

import src.readers.reader as reader


class ReadTokens(reader.Reader):
    def __init__(self, path=None, type_of_set='train'):
        super().__init__(path)
        self.ending = 'tokens'
        self.type_of_set = type_of_set

    def getting_data_from_files(self):
        if self.type_of_set == 'train':
            self.list_of_filenames = reader.Reader.trainset_filenames_list
        else:
            self.list_of_filenames = reader.Reader.testset_filenames_list
        self.inner_getting_data_from_files()
        return self.dic_of_files_with_dics

    def data_splitter(self, data):
        """
        :param data: rows from file
        :return: dict of tokens with params
        """
        tokens = {}
        for row in data:
            if row != '\n':
                entity = row.replace('\n', '').split(" ")
                tokens[entity[0]] = entity[1:]
        return tokens

    def get_random_data(self, start, end, step):
        random.shuffle(self.list_of_filenames)
        random_weights = random.randrange(start, end,
                                          step)  # trainset length is from 50% to 100% of corpus with the step 5
        weight_trainset = (int(len(self.list_of_filenames) * random_weights / 100))
        reader.Reader.trainset_filenames_list = self.list_of_filenames[:weight_trainset]
        reader.Reader.testset_filenames_list = self.list_of_filenames[int(len(self.list_of_filenames) * 0.75)
                                                                      + 1:]
