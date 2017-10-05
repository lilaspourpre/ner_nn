# -*- coding: utf-8 -*-
import psycopg2

import src.db.dbs_common as dbs


class DB_extract():
    def __init__(self, configfile):
        self.__db = dbs.SQL_query(configfile)
        self.__db.connect()
        self.__dic = {}

    def __get_objs(self):
        self.__db.cur.execute('SELECT span_ids, type, object_id FROM objects')
        self.__objects = self.__db.cur.fetchall()

    def get_tokens(self):
        self.__db.cur.execute("SELECT token_id, text_token, position FROM tokens WHERE token_id<>'NULL'")
        return self.__db.cur.fetchall()

    def get_tokens_params(self, token_id):
        self.__db.cur.execute("SELECT position, token_length FROM tokens WHERE token_id='"+token_id+"'")
        return self.__db.cur.fetchall()

    def get_files(self, tokens):
        condition = " OR ".join(["token_id='"+str(i)+"'" for i in tokens])
        self.__db.cur.execute("SELECT filename FROM files WHERE "+condition+";")
        return self.__db.cur.fetchall()

    def __get_spans(self):
        for obj in self.__objects:
            type_tag = obj[1]
            spans = obj[0].split(', ')
            len_spans = len(spans)
            for span in spans:
                self.__db.cur.execute("SELECT tokens_ids FROM spans WHERE span_id = '" + span + "';")
                tokens = self.__db.cur.fetchall()[0][0].split(' ')
                for token in tokens:
                    self.__db.cur.execute("SELECT token_id, text_token FROM tokens WHERE token_id = '"+token+"';")
                    result_ne = list(self.__db.cur.fetchall())[0]
                    try:
                        if self.__dic[token][3]<len_spans:
                            self.__dic[token] = [obj[2], result_ne[1], type_tag, len_spans]
                    except KeyError:
                        self.__dic[token] = [obj[2], result_ne[1], type_tag, len_spans]

    def close_db(self):
        try:
            self.__db.close()
        except psycopg2.DatabaseError as e:
            print(e)

    def get_dic(self):
        self.__get_objs() #we get all objs
        self.__get_spans()
        return self.__dic