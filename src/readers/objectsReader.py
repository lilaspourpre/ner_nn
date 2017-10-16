# -*- coding: utf-8 -*-
import codecs
import os
import src.readers.reader as reader


class Read_objs(reader.Reader):
    def __init__(self, path=None):
        super().__init__(path)

    def getting_data_from_files(self):
        self.list_of_filenames = list(map(lambda x: x.replace('.tokens', '.objects'),
                                          reader.Reader.trainset_filenames_list))
        self.inner_getting_data_from_files()
        return self.dic_of_files_with_dics

    def data_splitter(self, data):
        """
        :param data: rows from file
        :return: sends parsed lines to add_to_db function
        """
        objects = {}
        for row in data:
            entity = row.split(" # ")
            entity[1] = entity[1].replace('\n', '').split(' ')  # type ['141370', '141371', 'Восточной', 'Сибири'

            entity[0] = entity[0].split(' ')

            list_of_span_ids = []
            for index in range(1, len(entity[0])):
                if entity[0][index].upper() == entity[0][index]:
                    list_of_span_ids.append(entity[0][index])
                else:
                    tag_type = entity[0][index]
            list_of_rowdata = [tag_type, list_of_span_ids]
            list_of_rowdata.append(entity[1])
            objects[entity[0][0]] = list_of_rowdata
        return objects
