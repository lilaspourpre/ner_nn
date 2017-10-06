# -*- coding: utf-8 -*-
import src.bilou.to_bilou_tagging as to_bilou_tagging
import src.bilou.from_bilou_tagging as from_bilou_tagging
import src.db.db_exract as db_extract
import src.majorclass as maj_class
import src.result_writer as res_wr
import logging

class Pipeline():
    def __init__(self):
        self.mc = maj_class.MajorClass()

    def prep_stage(self):
        dbe = db_extract.DB_extract("config_dev.xml")  # calling class DB_extract
        dic = dbe.get_dic()  # type -->    dic = {token_id: [[object_id1, token_text, tag1],[object_id2, token_text, tag2]]}
        # TODO:(auto-division) for testing and training
        all_tokens = dbe.get_tokens()  # sql command "SELECT * from tokens"
        dbe.close_db()  # closing training DB
        return (dic, all_tokens)

    def training(self, dic, all_tokens):
        bilou = to_bilou_tagging.TO_BILOU(dic) #calling class BILOU with dic (for tagging)
        corpus = bilou.tag(all_tokens) #tagging all tokens returning a corpus
        bilou.writing_to_file() #optional, just to see what we have
        logging.log(logging.INFO, 'dic of NEs created')
        self.mc.fit(corpus)

    def getting_testset(self):
        dbe = db_extract.DB_extract("config_test.xml")
        # TODO:(auto-division) for testing and training
        all_tokens = dbe.get_tokens()
        return all_tokens

    def testing(self, test_set):
        unbilou = from_bilou_tagging.FROM_BILOU() #calling class FROMBILOU
        predicted = self.mc.predict(test_set) #predicting tags
        if len(test_set)==len(predicted): #if it's ok
            result = unbilou.untag(test_set, predicted) #we untag tokens
            unbilou.writing_to_file() #result with tags and words
            return result
        else:
            logging.log(logging.ERROR, 'lenght of test_set != predicted tags')

    def writing_to_file(self, result=None):
        #dic_res = {zip(['1757939', '1757940']): 'Person', zip(['1757939', '1757940']): 'Person'}
        res_wr.appending_res(result)

if __name__ == '__main__':
    res_wr.initialize_logger()
    pipeline = Pipeline()

    dic, all_tokens = pipeline.prep_stage()
    pipeline.training(dic, all_tokens)
    logging.log(logging.INFO, 'Training finished')
    test_set = pipeline.getting_testset()
    result_nes = pipeline.testing(test_set)
    logging.log(logging.INFO, 'Testing finished')
    pipeline.writing_to_file(result_nes)


