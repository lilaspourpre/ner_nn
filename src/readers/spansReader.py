# -*- coding: utf-8 -*-
import src.readers.reader as reader


class Read_spans(reader.Reader):
    def __init__(self, path=None):
        super().__init__(path)

    def getting_data_from_files(self):
        self.list_of_filenames = list(map(lambda x: x.replace('.tokens','.spans'),
                                          reader.Reader.trainset_filenames_list))
        self.inner_getting_data_from_files()
        return self.dic_of_files_with_dics

    def data_splitter(self, data):
        """
        :param data: rows from file
        :return: sends parsed lines to add_to_db function
        """
        spans = {}
        for row in data:
            entity = row.split(" # ")
            entity[1] = entity[1].replace('\n', '').split(' ')  # type ['141370', '141371', 'Восточной', 'Сибири'
            entity[0] = entity[0][0:-1].split(' ')
            list_of_rowdata = entity[0][1:]
            ids = []
            names = []
            for element in entity[1]:
                try:
                    ids.append(int(element))
                except ValueError as e:
                    names.append(element)
            list_of_rowdata.append(list(map(lambda x: str(x), ids)))
            list_of_rowdata.append(names)
            spans[entity[0][0]] = list_of_rowdata
        return spans