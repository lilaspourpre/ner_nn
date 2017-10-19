import argparse

import src.ner as ner


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-a", "--algorythm", help='"majorclass" or "random" options are available')
    parser.add_argument("-i", "--input_path", help="path to the input files directory")
    parser.add_argument("-o", "--output_path", help="path to the output files directory")

    args = parser.parse_args()
    if args.algorythm != 'majorclass' and args.algorythm != 'random':
        raise argparse.ArgumentTypeError('Value has to be "majorclass" or "random"')

    pipeline = ner.NerPipeline()
    pipeline.ner(type_of_algorythm=args.algorythm, source_path=args.input_path, output_path=args.output_path)


if __name__ == "__main__":
    main()
