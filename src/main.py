# -*- coding: utf-8 -*-
import argparse
from datetime import datetime
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
from enitites.features.prefix_feature import PrefixFeature
from enitites.features.suffix_feature import SuffixFeature
from enitites.features.if_no_lowercase import LowerCaseFeature
from enitites.features.gazetteer import GazetterFeature
from machine_learning.majorclass_model_trainer import MajorClassModelTrainer
from machine_learning.random_model_trainer import RandomModelTrainer
from machine_learning.svm_model_trainer import SvmModelTrainer
from reader import get_documents_with_tags_from, get_documents_without_tags_from


# ********************************************************************
#       Main function
# ********************************************************************



def main():
    print(datetime.now())
    args = parse_arguments()
    morph_analyzer = pymorphy2.MorphAnalyzer()
    output_path = os.path.join(args.output_path, datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))

    train_documents = get_documents_with_tags_from(args.trainset_path, morph_analyzer)
    print('Docs are ready for training', datetime.now())
    test_documents = get_documents_without_tags_from(args.testset_path, morph_analyzer)
    print('Docs are ready for testing', datetime.now())

    prefixes = __compute_affixes(train_documents, end=args.ngram_affixes)
    suffixes = __compute_affixes(train_documents, start=-args.ngram_affixes)

    model_trainer, feature = choose_model(args.algorythm, args.window, prefixes=prefixes, suffixes=suffixes)
    train_and_compute_nes_from(model_trainer=model_trainer, feature=feature, train_documents=train_documents,
                               test_documents=test_documents, output_path=output_path)
    print("Testing finished", datetime.now())
    print('Output path: \n {}'.format(output_path))


# --------------------------------------------------------------------

def parse_arguments():
    """
    :return: args (arguments)
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("-a", "--algorythm", help='"majorclass", "svm" or "random" options are available',
                        required=True)
    parser.add_argument("-w", "--window", help='window size for context', default=2)
    parser.add_argument("-n", "--ngram_affixes", help='number of n-gramns for affixes', default=3)
    parser.add_argument("-t", "--trainset_path", help="path to the trainset files directory")
    parser.add_argument("-s", "--testset_path", help="path to the testset files directory")
    parser.add_argument("-o", "--output_path", help="path to the output files directory",
                        default=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output'))

    args = parser.parse_args()
    return args


# --------------------------------------------------------------------


def __compute_affixes(documents, start=None, end=None):
    set_of_affixes = set()
    for document in documents.values():
        for token in document.get_token_texts():
            set_of_affixes.update([token[start:end]]) # XXX why update with list and not add single element?
    return tuple(set_of_affixes) # XXX why tuple?


# --------------------------------------------------------------------

def choose_model(method, window, prefixes, suffixes):
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
        feature = get_composite_feature(window, prefixes, suffixes)
        return SvmModelTrainer(kernel=None), feature
    else:
        raise argparse.ArgumentTypeError('Value has to be "majorclass" or "random" or "svm"')


def get_composite_feature(window, prefixes, suffixes):
    """
    Adding features to composite
    :return: composite (feature storing features)
    """

    list_of_features = [LengthFeature(), NumbersInTokenFeature(), PositionFeature(), ConcordCaseFeature(), DFFeature(),
                        LettersFeature(), GazetterFeature(), LowerCaseFeature(), SpecCharsFeature(),
                        StopWordsFeature(), PrefixFeature(prefixes), SuffixFeature(suffixes)] # XXX Is it going to work, if I use non-default affix n-grams
    basic_features = [POSFeature(), CaseFeature(), MorphoCaseFeature(), PunctFeature()]
    for feature in basic_features:
        for offset in range(-window, window + 1):
            list_of_features.append(ContextFeature(feature, offset))
    composite = FeatureComposite(list_of_features)
    return composite


# --------------------------------------------------------------------

def train_and_compute_nes_from(model_trainer, feature, train_documents, test_documents, output_path):
    """
    :param model_trainer:
    :param feature:
    :param documents:
    :param testset_path:
    :param output_path:
    :param morph_analyzer:
    :return:
    """
    model = trainer.train(model_trainer, feature, train_documents)
    print("Training finished", datetime.now())
    ne_creator.compute_nes(test_documents, feature, model, output_path)


if __name__ == '__main__':
    main()
