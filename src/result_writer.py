# -*- coding: utf-8 -*-
import codecs, logging
import csv, os.path, datetime
import src.db.db_exract as db_extract

def initialize_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to info
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(levelname)s: %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def appending_res(dic_res):
    folder = os.path.dirname(__file__)
    res_folder = folder.replace(os.path.basename(folder), 'result'+str(datetime.datetime.now().strftime(' %Y-%m-%d %H-%M-%S')))
    if not os.path.exists(res_folder):
        os.makedirs(res_folder)
    dbe = db_extract.DB_extract("config_test.xml")
    for entity in dic_res.keys():
        list_of_tokens = list(i[0] for i in entity)
        dbe_res = dbe.get_files(list_of_tokens)
        if len(set(dbe_res)) == 1:
            filename = dbe_res[0][0]
            logging.log(logging.INFO, filename)
            list_of_params = []
            for token_id in list_of_tokens:
                dbe_params = dbe.get_tokens_params(token_id)
                list_of_params.extend(dbe_params)
            entity_length = len(list_of_params)-1+sum([int(i[1]) for i in list_of_params])
            res_filename = os.path.join(res_folder, filename.split('.')[0]+'.result')
            with codecs.open(res_filename, 'a', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=' ')
                writer.writerow([dic_res[entity],list_of_params[0][0], str(entity_length)])

        else:
            print(dbe_res)
            logging.log(logging.ERROR, 'problems with db')
            raise Exception
