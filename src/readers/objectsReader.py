# -*- coding: utf-8 -*-
import codecs
import os

import psycopg2

import src.db.dbs_common as dbs


class Read_objs():
    def __init__(self, folder):
        self.folder = os.path.dirname(os.path.dirname(__file__)) # lambda
        self.folder = self.folder.replace(os.path.basename(self.folder), os.path.join('data', folder))  # lambda
        self.list_of_files = [] #list of files will be here
        self.entities = []
        self.counter = 0

    def getting_filenames(self, type):
        """
        getting files with the correct ending from directory
        :return: saving them to self.list_of_files
        """
        for root, dirs, files in os.walk(self.folder):
            for file in files: #for each file in folder
                if file.endswith(type): #if it ends with .objects
                    self.list_of_files.append(os.path.join(root, file)) #we add it to the list of files

    def search_in_file(self, what_to_search):
        for file in self.list_of_files:
            with codecs.open(file, 'r', encoding='utf-8') as f:
                if what_to_search in f.read():
                    print(file)


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
        self.counter += len(data)
        for i in data:
            entity = i.split(" # ")
            entity[1] = entity[1].replace('\n', '')  # type 'Соединенные Штаты'
            entity[0] = entity[0].replace('LocOrg', 'Location').split(
                ' ')
            entity = (entity[0][0], entity[0][1], ', '.join(entity[0][2::]), entity[1])
            self.entities.append(entity)


    def add_to_db(self, query, configfile):
        """
        :param entities: list of NE with params (list in list)
        :return: added to db info
        """
        sql = dbs.SQL_query(configfile)
        sql.connect()
        records_list_template = ','.join(['%s'] * len(self.entities))
        insert_query = query.format(
            records_list_template)
        sql.cur.execute(insert_query, self.entities)
        sql.con.commit()
        try:
            sql.close()
        except psycopg2.DatabaseError as e:
            print(e)

# new_NER = Read_objs('testset')
# new_NER.getting_filenames(".objects")
# new_NER.getting_data_from_files()
# print(new_NER.counter)
# new_NER.add_to_db('insert into objects (object_id, type, span_ids, objects_texts) values {}', 'config_test.xml')