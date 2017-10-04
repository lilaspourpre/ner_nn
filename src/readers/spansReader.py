# -*- coding: utf-8 -*-
import codecs
import re

import src.readers.objectsReader as r_objs


class Read_spans(r_objs.Read_objs):
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
            entity = i.split(" # ")
            entity[1] = entity[1].replace('\n', '')  # type '141370 141371 Восточной Сибири'
            reg_ex = re.compile('[\d]{5,7}')
            ids = ' '.join(reg_ex.findall(entity[1]))
            entity[0] = entity[0][0:-1].split(' ')
            list_of_rowdata = []
            list_of_rowdata.extend(entity[0])
            list_of_rowdata.append(ids)
            self.entities.append(tuple(list_of_rowdata))

# new_spans_r = Read_spans('testset')
# new_spans_r.getting_filenames(".spans")
# new_spans_r.getting_data_from_files()
# new_spans_r.add_to_db('insert into spans (span_id, type, position, length_in_symbols, first_char, length_in_tokens, tokens_ids) values {}', 'config_test.xml')