# -*- coding: utf-8 -*-
import codecs

import src.readers.objectsReader as r_objs


class Read_tokens(r_objs.Read_objs):
    def __init__(self, folder):
        super().__init__(folder)

    def getting_data_from_files(self):
        """
        reading from each file from list and sending text to the data splitter
        :return: None
        """
        for file in self.list_of_files:
            with codecs.open(file, 'r', encoding='utf-8') as f:
                self.data_splitter(f.readlines())

    def data_splitter(self, data):
        """
        :param data: rows from file
        :return: sends parsed lines to add_to_db function
        """
        for i in data:
            if i!='\n':
                entity = i.replace('\n', '').split(" ")
                self.entities.append(tuple(entity))
            else:
                self.entities.append(('NULL', 'NULL', 'NULL', i))



new_spans_r = Read_tokens('testset')
new_spans_r.getting_filenames(".tokens")
new_spans_r.getting_data_from_files()
new_spans_r.add_to_db('insert into tokens (token_id, position, token_length, text_token) values {}', 'config_test.xml')