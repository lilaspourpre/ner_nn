# -*- coding: utf-8 -*-
import psycopg2, time, os
import xml.etree.ElementTree as ET

class SQL_query():
    """
    класс, который осуществляет поиск в базе данных
    поддерживает возможность поиска информации и добаления новых данных (insert)
    """
    def __init__(self, configfile):
        self.con = None
        self.cur = None
        self.configfile = configfile
        self.DB_RECONNECT_DELAY_SEC = 1

    def open_config(self, config): #находит в файле xml код и строит дерево, возвращает строку для коннекта
        tree = ET.parse(config)
        root = tree.getroot()
        string = ""
        for child in root: #соединяем данные в строку user=postgres и тд
            string+=child.tag+"='"+child.text+"' "
        return string

    def connect(self): #подключение к БД
        try:
            folder = os.path.dirname(__file__)
            cfg_file = folder.replace(os.path.basename(folder), os.path.join("config", self.configfile))
            self.con = psycopg2.connect(self.open_config(cfg_file))
            self.cur = self.con.cursor()
        except psycopg2.DatabaseError as e:
            if self.con:
                self.con.rollback()

    def close(self): #отключение от БД
        if self.con:
            self.con.close()

    def ensure_connection(self):
        while not self.con:
            self.connect()
            if not self.con:
            # wait for a second
                time.sleep(self.DB_RECONNECT_DELAY_SEC)

RP = SQL_query("config_test.xml")
RP.connect()
# RP.cur.execute('DELETE FROM spans')
# RP.cur.execute('DELETE FROM tokens')
# RP.cur.execute('DELETE FROM objects')
RP.cur.execute('CREATE TABLE IF NOT EXISTS files (token_id varchar NOT NULL, filename varchar NOT NULL, CONSTRAINT Pk_files PRIMARY KEY (token_id, filename))')
#
# RP.cur.execute('CREATE TABLE IF NOT EXISTS tokens (id serial8 NOT NULL, token_id varchar NOT NULL, position varchar NOT NULL, token_length varchar NOT NULL, text_token varchar NOT NULL, CONSTRAINT Pk_tokens PRIMARY KEY (id))')
# RP.cur.execute('CREATE TABLE IF NOT EXISTS spans (id serial8 NOT NULL, span_id varchar NOT NULL, type varchar NOT NULL, position varchar NOT NULL, length_in_symbols varchar NOT NULL, first_char varchar NOT NULL, length_in_tokens varchar NOT NULL, tokens_ids varchar NOT NULL, CONSTRAINT Pk_spans PRIMARY KEY (id))')
# RP.cur.execute('CREATE TABLE IF NOT EXISTS objects (id serial8 NOT NULL, object_id varchar NOT NULL, type varchar NOT NULL, span_ids varchar NOT NULL, objects_texts varchar NOT NULL, CONSTRAINT Pk_objs PRIMARY KEY (id))')
RP.con.commit()
try:
    RP.close()
except psycopg2.DatabaseError as e:
    print(e)

