# -*- coding: utf-8 -*-
import argparse
import datetime
import os
import pymorphy2
import trainer
import ne_creator
from enitites.features.composite import FeatureComposite
from enitites.features.part_of_speech import POSFeature
from enitites.features.length import LengthFeature
from enitites.features.numbers import NumbersInTokenFeature
from enitites.features.case import CaseFeature
from enitites.features.morpho_case import MorphoCaseFeature
from enitites.features.context_feature import ContextFeature
from enitites.features.special_chars import SpecCharsFeature
from enitites.features.letters import LettersFeature
from enitites.features.df import DFFeature
from enitites.features.position_in_sentence import PositionFeature
from enitites.features.not_in_stop_words import StopWordsFeature
from enitites.features.case_concordance import ConcordCaseFeature
from enitites.features.punctuation import PunctFeature
from enitites.features.affix_feature import AffixFeature
from enitites.features.if_no_lowercase import LowerCaseFeature
from enitites.features.gazetteer import GazetterFeature
from machine_learning.majorclass_model_trainer import MajorClassModelTrainer
from machine_learning.random_model_trainer import RandomModelTrainer
from machine_learning.svm_model_trainer import SvmModelTrainer


# ********************************************************************
#       Main function
# ********************************************************************


def main():
    print(datetime.datetime.now())
    args = parse_arguments()
    model_trainer, feature = choose_model(args.algorythm, args.window)
    output_path = train_and_compute_nes_from(model_trainer=model_trainer, feature=feature,
                                             trainset_path=args.trainset_path,
                                             testset_path=args.testset_path, output_path=args.output_path,
                                             morph_analyzer=pymorphy2.MorphAnalyzer(), ngram_affixes=args.ngram_affixes)
    print(output_path)
    print(datetime.datetime.now())


# --------------------------------------------------------------------

def parse_arguments():
    """
    :return: args (arguments)
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("-a", "--algorythm", help='"majorclass", "svm" or "random" options are available',
                        required=True)
    parser.add_argument("-w", "--window", help='window size for context', default=2)
    parser.add_argument("-n", "--ngram_affixes", help='number of n-gramns for affixes', default=2)
    parser.add_argument("-t", "--trainset_path", help="path to the trainset files directory")
    parser.add_argument("-s", "--testset_path", help="path to the testset files directory")
    parser.add_argument("-o", "--output_path", help="path to the output files directory",
                        default=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output'))

    args = parser.parse_args()
    return args


# --------------------------------------------------------------------

def choose_model(method, window):
    """
    :param window:
    :param method: method from argparse
    :return: model trainer + composite
    """
    if method == 'majorclass':
        return MajorClassModelTrainer(), FeatureComposite()
    elif method == 'random':
        return RandomModelTrainer(), FeatureComposite()
    elif method == 'svm':
        feature = get_composite_feature(window)
        return SvmModelTrainer(kernel=None), feature
    else:
        raise argparse.ArgumentTypeError('Value has to be "majorclass" or "random" or "svm"')


def get_composite_feature(window):
    """
    Adding features to composite
    :return: composite (feature storing features)
    """
    list_of_features = [LengthFeature(), NumbersInTokenFeature(), PositionFeature(), ConcordCaseFeature(), DFFeature(),
                        LettersFeature(), GazetterFeature(), LowerCaseFeature(), SpecCharsFeature(), StopWordsFeature(),
                        AffixFeature(check_preffixes=True), AffixFeature(check_preffixes=False), PunctFeature()]
    basic_features = [POSFeature(), CaseFeature(), MorphoCaseFeature()]
    for feature in basic_features:
        for offset in range(-window, window + 1):
            list_of_features.append(ContextFeature(feature, offset))
    composite = FeatureComposite(list_of_features)
    return composite


# --------------------------------------------------------------------

def train_and_compute_nes_from(model_trainer, feature, trainset_path, testset_path, output_path, morph_analyzer,
                               ngram_affixes):
    """
    :param model_trainer:
    :param feature:
    :param trainset_path:
    :param testset_path:
    :param output_path:
    :param morph_analyzer:
    :return:
    """
    model = trainer.train(model_trainer, feature, morph_analyzer, ngram_affixes, trainset_path)
    print("Training finished", datetime.datetime.now())
    return ne_creator.compute_nes(testset_path, feature, model, output_path, morph_analyzer)


if __name__ == '__main__':
    main()
