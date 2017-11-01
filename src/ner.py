# -*- coding: utf-8 -*-
import os
import logging
import codecs
import csv
from src import trainer
from src import ne_creator



def get_nes_from(method, trainset_path, testset_path):
    logging.log(logging.INFO, "START OF GETTING NEs")
    model = trainer.trainer(method, trainset_path)
    nes = ne_creator.compute_nes(testset_path, model)
    return nes


def write_to_file(nes, path):
    #TODO: to be reviewed
    if not os.path.exists(path):
        os.makedirs(path)

    for file in nes:
        logging.log(logging.INFO, 'Writing to ' + file)
        with codecs.open(file + ".task1", 'a', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=' ')
            for ne in file:
                writer.writerow(ne)
