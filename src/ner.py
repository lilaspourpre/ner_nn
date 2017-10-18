# -*- coding: utf-8 -*-
import src.bilou.to_bilou_tagging as to_bilou_tagging
import src.bilou.from_bilou_tagging as from_bilou_tagging
import src.readers.tokensReader as tokensReader
import src.readers.spansReader as spansReader
import src.readers.objectsReader as objectsReader
import src.majorclass as maj_class
import src.result_writer as result_writer
import logging
import src.dictionary_extraction as dict_extraction
import sys


class NerPipeline:
    def __init__(self):
        self.mc = maj_class.MajorClass()
        self.trainset_tokens = None
        self.testset_tokens = None
        self.trainset_spans = None
        self.trainset_objects = None
        self.dic_of_nes = None
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(levelname)s: %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    def prep_stage(self, source_path):

        train_tokens = tokensReader.ReadTokens(path=source_path)
        train_tokens.getting_filenames('.tokens')
        train_tokens.get_random_data(50, 100, 5)  # trainset length is from 50% to 100% of corpus

        self.trainset_tokens = train_tokens.getting_data_from_files()
        test_tokens = tokensReader.ReadTokens(type_of_set='test', path=source_path)
        self.testset_tokens = test_tokens.getting_data_from_files()

        train_spans = spansReader.ReadSpans(path=source_path)
        self.trainset_spans = train_spans.getting_data_from_files()

        train_objects = objectsReader.ReadObjs(path=source_path)
        self.trainset_objects = train_objects.getting_data_from_files()

        d_e = dict_extraction.DictionaryBuilding(self.trainset_spans,
                                                 self.trainset_objects)  # calling class DB_extract
        self.dic_of_nes = d_e.get_dic()

    def training(self, type_of_algorythm, source_path=None):
        bilou = to_bilou_tagging.ToBILOU(self.dic_of_nes)  # calling class BILOU with dic (for tagging)
        corpus = bilou.tag(self.trainset_tokens)  # tagging all tokens returning a corpus
        bilou.writing_to_file()  # optional, just to see what we have
        logging.log(logging.INFO, 'Named Entities are tagged')
        self.mc.fit(corpus, type_of_algorythm)

    def testing(self):
        unbilou = from_bilou_tagging.FromBILOU()  # calling class FROMBILOU
        predicted = self.mc.predict(self.testset_tokens)  # predicting tags
        if len(self.testset_tokens) == len(predicted):  # if it's ok
            if len(self.testset_tokens.keys()) == len(predicted.keys()):
                result = unbilou.untag(self.testset_tokens, predicted)  # we untag tokens
                unbilou.writing_to_file()  # result with tags and words
                return result
            else:
                print(len(self.testset_tokens.keys()))
                print(len(predicted.keys()))
                logging.log(logging.ERROR, 'lenght of inner test_set != predicted tags')
        else:
            logging.log(logging.ERROR, 'lenght of outer test_set != predicted tags')

    def writing_to_file(self, result=None, path=None):
        result_writer.to_file(self.testset_tokens, result, path)

    def ner(self, type_of_algorythm, source_path=None, output_path=None):
        print(type_of_algorythm)
        self.prep_stage(source_path=source_path)
        logging.log(logging.INFO, 'Prep stage finished')
        logging.log(logging.INFO, 'Training started')
        self.training(type_of_algorythm)
        logging.log(logging.INFO, 'Training finished')
        logging.log(logging.INFO, 'Testing started')
        result_named_entities = self.testing()
        logging.log(logging.INFO, 'Testing finished')
        self.writing_to_file(result=result_named_entities, path=output_path)
