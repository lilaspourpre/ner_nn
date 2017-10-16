# -*- coding: utf-8 -*-
import src.bilou.to_bilou_tagging as to_bilou_tagging
import src.bilou.from_bilou_tagging as from_bilou_tagging
import src.readers.tokensReader as tokens_reader
import src.readers.spansReader as spans_reader
import src.readers.objectsReader as objects_reader
import src.majorclass as maj_class
import src.result_writer as result_writer
import logging
import src.dictionary_extraction as dict_extraction


class NER_Pipeline():
    def __init__(self):
        self.mc = maj_class.MajorClass()

        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(levelname)s: %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    def prep_stage(self):

        train_tokens = tokens_reader.Read_tokens()
        train_tokens.getting_filenames('.tokens')
        train_tokens.get_random_data(50, 100, 5)  # trainset length is from 50% to 100% of corpus

        self.trainset_tokens = train_tokens.getting_data_from_files()
        test_tokens = tokens_reader.Read_tokens(type_of_set='test')
        self.testset_tokens = test_tokens.getting_data_from_files()

        train_spans = spans_reader.Read_spans()
        self.trainset_spans = train_spans.getting_data_from_files()

        train_objects = objects_reader.Read_objs()
        self.trainset_objects = train_objects.getting_data_from_files()

        # logging.log(logging.INFO, self.trainset_spans)
        # logging.log(logging.INFO, self.trainset_objects)
        # logging.log(logging.INFO, self.trainset_tokens)

        d_e = dict_extraction.Dictionary_building(self.trainset_spans, self.trainset_objects)  # calling class DB_extract
        self.dic = d_e.get_dic()

    def training(self):
        bilou = to_bilou_tagging.TO_BILOU(self.dic)  # calling class BILOU with dic (for tagging)
        corpus = bilou.tag(self.trainset_tokens)  # tagging all tokens returning a corpus
        bilou.writing_to_file()  # optional, just to see what we have
        logging.log(logging.INFO, 'Named Entities are tagged')
        # self.mc.fit(corpus)

    def testing(self, test_set):
        unbilou = from_bilou_tagging.FROM_BILOU()  # calling class FROMBILOU
        predicted = self.mc.predict(test_set)  # predicting tags
        if len(test_set) == len(predicted):  # if it's ok
            result = unbilou.untag(test_set, predicted)  # we untag tokens
            unbilou.writing_to_file()  # result with tags and words
            return result
        else:
            logging.log(logging.ERROR, 'lenght of test_set != predicted tags')

    def writing_to_file(self, result=None):
        # dic_res = {zip(['1757939', '1757940']): 'Person', zip(['1757939', '1757940']): 'Person'}
        result_writer.to_file(result)

    def ner(self):
        self.prep_stage()
        logging.log(logging.INFO, 'Prep stage finished')
        logging.log(logging.INFO, 'Training started')
        self.training()
        # logging.log(logging.INFO, 'Training finished')
        # test_set = self.getting_testset()
        # result_named_entities = self.testing(testset)
        # logging.log(logging.INFO, 'Testing finished')
        # logging.log(logging.INFO, result_named_entities)
        # pipeline.writing_to_file(result_named_entities)


if __name__ == '__main__':
    pipeline = NER_Pipeline()
    pipeline.ner()
