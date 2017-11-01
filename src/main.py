# -*- coding: utf-8 -*-
import argparse
import logging
from src.ner import get_nes_from
from src.ner import write_to_file


def main():
    """
    Parsing arguments
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("-a", "--algorythm", help='"majorclass" or "random" options are available')
    parser.add_argument("-t", "--trainset_path", help="path to the trainset files directory")
    parser.add_argument("-s", "--testset_path", help="path to the testset files directory")
    parser.add_argument("-o", "--output_path", help="path to the output files directory")

    args = parser.parse_args()
    if args.algorythm != 'majorclass' and args.algorythm != 'random' and args.algorythm != 'svm':
        raise argparse.ArgumentTypeError('Value has to be "majorclass" or "random" or "svm"')

    """
    Calling logger
    """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(levelname)s: %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    """
    Getting NEs and writing them to file
    """
    nes = get_nes_from(method=args.algorythm, trainset_path=args.trainset_path, testset_path=args.testset_path)
    write_to_file(nes, args.output_path)


if __name__ == '__main__':
    main()
