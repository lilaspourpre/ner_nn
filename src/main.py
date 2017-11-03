# -*- coding: utf-8 -*-
import argparse
import logging
import os
import logging
import codecs
import csv
from src import trainer
from src import ne_creator


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
    nes = get_nes_from(method=args.algorythm, trainset_path=args.trainset_path, testset_path=args.testset_path)
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
    if args.algorythm != 'majorclass' and args.algorythm != 'random' and args.algorythm != 'svm':
        raise argparse.ArgumentTypeError('Value has to be "majorclass" or "random" or "svm"')
    return args


def get_nes_from(method, trainset_path, testset_path):
    """
    :param method: method to train model
    :param trainset_path: path where the devset is
    :param testset_path: path where the testset is
    :return: named entities
    """
    logging.log(logging.INFO, "START OF GETTING NEs")
    model = trainer.train(method, trainset_path)
    nes = ne_creator.compute_nes(testset_path, model)
    return nes


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
