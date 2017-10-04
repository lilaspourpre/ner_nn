# -*- coding: utf-8 -*-
import codecs
import os

import src.readers.objectsReader as r_objs


class Read_files(r_objs.Read_objs):
    def __init__(self, folder):
        super().__init__(folder)

    def getting_data_from_files(self):
        """
        reading from each file from list and sending text to the data splitter
        :return: None
        """
        for file in self.list_of_files:
            with codecs.open(file, 'r', encoding='utf-8') as f:
                self.data_extraction(f.readlines(), os.path.basename(file))

    def data_extraction(self, data, filename):
        """
        :param data: rows from file
        :filename:
        :return: sends parsed lines to add_to_db function
        """
        for i in data:
            if i!='\n':
                entity = i.replace('\n', '').split(" ")
                self.entities.append((entity[0], filename))

new_spans_r = Read_files('testset')
new_spans_r.getting_filenames(".tokens")
new_spans_r.getting_data_from_files()
new_spans_r.add_to_db('insert into files (token_id, filename) values {}', 'config_test.xml')