# -*- coding: utf-8 -*-
import argparse
import os
from src import trainer
from src import ne_creator
from src.enitites.features.composite import FeatureComposite
from src.enitites.features.part_of_speech import POSFeature
from src.enitites.features.length import LengthFeature
from src.enitites.features.case import CaseFeature
from src.enitites.features.morpho_case import MorphoFeature
from src.enitites.features.context_feature import ContextFeature
from src.machine_learning.majorclass_model_trainer import MajorClassModelTrainer
from src.machine_learning.random_model_trainer import RandomModelTrainer
from src.machine_learning.svm_model_trainer import SvmModelTrainer
from datetime import datetime



# ********************************************************************
#       Main function
# ********************************************************************


def main():
    args = parse_arguments()
    trainer, feature = choose_model(args.algorythm, args.window)
    output_path = train_and_compute_nes_from(model_trainer=trainer, feature=feature, trainset_path=args.trainset_path,
                               testset_path=args.testset_path, output_path=args.output_path)
    print(output_path)


# --------------------------------------------------------------------

def parse_arguments():
    """
    :return: args (arguments)
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("-a", "--algorythm", help='"majorclass", "svm" or "random" options are available', required=True)
    parser.add_argument("-w", "--window", help='window size for context', default=2)
    parser.add_argument("-t", "--trainset_path", help="path to the trainset files directory")
    parser.add_argument("-s", "--testset_path", help="path to the testset files directory")
    parser.add_argument("-o", "--output_path", help="path to the output files directory",
                        default=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output'))

    args = parser.parse_args()
    return args


# --------------------------------------------------------------------

def choose_model(method, window):
    """
    :param method: method from argparse
    :return: model trainer + composite
    """
    if method == 'majorclass':
        return MajorClassModelTrainer(), FeatureComposite()
    elif method == 'random':
        return RandomModelTrainer(), FeatureComposite()
    elif method == 'svm':
        feature = get_composite_feature(window)
        return SvmModelTrainer(decision_function_shape='ovo', kernel=None), feature
    else:
        raise argparse.ArgumentTypeError('Value has to be "majorclass" or "random" or "svm"')


def get_composite_feature(window):
    """
    Adding features to composite
    :return: composite (feature storing features)
    """
    list_of_features = [LengthFeature()]
    basic_features = [POSFeature(), CaseFeature(), MorphoFeature()]
    for feature in basic_features:
        for offset in range(-window, window + 1):
            list_of_features.append(ContextFeature(feature, offset))
    composite = FeatureComposite(list_of_features)
    return composite


# --------------------------------------------------------------------

def train_and_compute_nes_from(model_trainer, feature, trainset_path, testset_path, output_path):
    """
    :param method: method to train model
    :param trainset_path: path where the devset is
    :param testset_path: path where the testset is
    :return: named entities
    """
    model = trainer.train(model_trainer, feature, trainset_path)
    return ne_creator.compute_nes(testset_path, feature, model, output_path)


if __name__ == '__main__':
    main()
