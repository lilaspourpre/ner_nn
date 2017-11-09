# -*- coding: utf-8 -*-
import argparse
import os
import logging
import codecs
import csv
from src import trainer
from src import ne_creator
from src.machine_learning.majorclass_model_trainer import MajorClassModelTrainer
from src.machine_learning.random_model_trainer import RandomModelTrainer
from src.machine_learning.svm_model_trainer import SvmModelTrainer


def initiate_logger():
    """
    Initiate logger
    """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(levelname)s: %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def main():
    args = parse_arguments()
    model_trainer = choose_model(args.algorythm)
    nes = train_and_compute_nes_from(model_trainer=model_trainer, trainset_path=args.trainset_path,
                                     testset_path=args.testset_path)
    write_to_file(nes, args.output_path)


def parse_arguments():
    """
    :return: args (arguments)
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("-a", "--algorythm", help='"majorclass" or "random" options are available')
    parser.add_argument("-t", "--trainset_path", help="path to the trainset files directory")
    parser.add_argument("-s", "--testset_path", help="path to the testset files directory")
    parser.add_argument("-o", "--output_path", help="path to the output files directory")

    args = parser.parse_args()
    return args


def train_and_compute_nes_from(model_trainer, trainset_path, testset_path):
    """
    :param method: method to train model
    :param trainset_path: path where the devset is
    :param testset_path: path where the testset is
    :return: named entities
    """
    logging.log(logging.INFO, "START OF GETTING NEs")
    model = trainer.train(model_trainer, trainset_path)
    print(model)
    exit(0)
    nes = ne_creator.compute_nes(testset_path, model)
    return nes

def choose_model(method):
    if method == 'majorclass':
        return MajorClassModelTrainer(), []
    elif method == 'random':
        return RandomModelTrainer(), []
    elif method == 'svm':
        return SvmModelTrainer(decision_function_shape='ovo', kernel=None), get_feature_list()
    else:
        raise argparse.ArgumentTypeError('Value has to be "majorclass" or "random" or "svm"')

def get_feature_list():
    list_of_features = []
    list_of_features.append(1)
    list_of_features.append(1)
    list_of_features.append(1)
    return list_of_features

def write_to_file(nes, path):
    """
    :param nes: nes to write
    :param path: path where to write
    :return: None
    """
    # TODO: to be reviewed
    if not os.path.exists(path):
        os.makedirs(path)
    for file in nes:
        logging.log(logging.INFO, 'Writing to ' + file)
        with codecs.open(file + ".task1", 'a', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=' ')
            for ne in file:
                writer.writerow(ne)


if __name__ == '__main__':
    initiate_logger()
    main()
