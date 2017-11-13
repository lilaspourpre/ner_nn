# -*- coding: utf-8 -*-
import argparse
import os
import logging
import codecs
import csv
from src import trainer
from src import ne_creator
from src.enitites.features.composite import FeatureComposite
from src.enitites.features.part_of_speech import POSFeature
from src.enitites.features.position import PositionFeature
from src.enitites.features.length import LengthFeature
from src.enitites.features.case import CaseFeature
from src.enitites.features.morpho_case import MorphoFeature
from src.enitites.features.next_case import NextCaseFeature
from src.enitites.features.previous_case import PrevCaseFeature
from src.enitites.features.next_morpho_case import NextMorphoCaseFeature
from src.enitites.features.previous_morpho_case import PrevMorphoCaseFeature
from src.enitites.features.next_pos import NextPOSFeature
from src.enitites.features.previous_pos import PrevPOSFeature
from src.machine_learning.majorclass_model_trainer import MajorClassModelTrainer
from src.machine_learning.random_model_trainer import RandomModelTrainer
from src.machine_learning.svm_model_trainer import SvmModelTrainer
from datetime import datetime




def initiate_logger():
    """
    Initiate logger
    """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    dir_to_write = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
    if not os.path.exists(dir_to_write):
        os.mkdir(dir_to_write)
    file_to_write = os.path.join(dir_to_write, datetime.now().strftime("%Y-%m-%d %H-%M-%S") + '.txt')
    handler2 = logging.FileHandler(filename=file_to_write)
    formatter = logging.Formatter("%(levelname)s: %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    handler2.setFormatter(formatter)
    logger.addHandler(handler2)


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
    logging.log(logging.INFO, "MODEL " + repr(model) + " SUCCESSFULLY CREATED")
    exit(0)
    nes = ne_creator.compute_nes(testset_path, model)
    return nes

def choose_model(method):
    if method == 'majorclass':
        return MajorClassModelTrainer(), FeatureComposite()
    elif method == 'random':
        return RandomModelTrainer(), FeatureComposite()
    elif method == 'svm':
        return SvmModelTrainer(decision_function_shape='ovo', kernel=None), get_feature_list()
    else:
        raise argparse.ArgumentTypeError('Value has to be "majorclass" or "random" or "svm"')

def get_feature_list():
    list_of_features = []
    list_of_features.append(POSFeature())
    list_of_features.append(PositionFeature())
    list_of_features.append(LengthFeature())
    list_of_features.append(CaseFeature())
    list_of_features.append(MorphoFeature())
    list_of_features.append(NextCaseFeature())
    list_of_features.append(PrevCaseFeature())
    list_of_features.append(NextPOSFeature())
    list_of_features.append(PrevPOSFeature())
    list_of_features.append(NextMorphoCaseFeature())
    list_of_features.append(PrevMorphoCaseFeature())
    composite = FeatureComposite(list_of_features)
    logging.log(logging.INFO, repr(composite))
    return composite

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
