# -*- coding: utf-8 -*-
import os
import codecs
from abc import abstractmethod


class Reader:
    trainset_filenames_list = []
    testset_filenames_list = []

    def __init__(self, path=None):
        if path is None:
            self.path = lambda x: x.replace(os.path.basename(x), os.path.join('data', 'devset'))
            self.path = self.path(os.path.dirname(os.path.dirname(__file__)))
        else:
            self.path = path
        self.list_of_filenames = []
        self.dic_of_files_with_dics = {}

    def getting_filenames(self, endswith):
        """
        getting files with the correct ending from directory
        :return: saving them to self.list_of_files
        """
        for root, dirs, files in os.walk(self.path):
            for file in files:  # for each file in folder
                if file.endswith(endswith):  # if it ends with .objects
                    self.list_of_filenames.append(os.path.join(root, file))  # we add it to the list of files

    def inner_getting_data_from_files(self):
        """
        reading from each file from list and sending text to the data splitter
        :return: None
        """
        for file in self.list_of_filenames:
            with codecs.open(file, 'r', encoding='utf-8') as f:
                dict_of_tokens = self.data_splitter(f.readlines())
                self.dic_of_files_with_dics[
                    file.replace('.spans', '').replace('.objects', '').replace('.tokens', '')] = dict_of_tokens

    @abstractmethod
    def getting_data_from_files(self):
        pass

    @abstractmethod
    def data_splitter(self, data):
        pass
