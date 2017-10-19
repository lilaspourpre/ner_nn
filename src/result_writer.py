# -*- coding: utf-8 -*-
import codecs
import logging
import csv
import os.path
import datetime


def to_file(testset, dic_of_files_with_results, path):
    if path is not None:
        if not os.path.exists(path):
            os.makedirs(path)
        res_folder = path
    else:
        folder = os.path.dirname(__file__)
        res_folder = folder.replace(os.path.basename(folder),
                                    'result_' + str(datetime.datetime.now().strftime('_%Y-%m-%d_%H-%M-%S')))
        if not os.path.exists(res_folder):
            os.makedirs(res_folder)

    for file in dic_of_files_with_results.keys():
        logging.log(logging.INFO, 'Writing to ' + file)
        for token_tuple in dic_of_files_with_results[file].keys():
            length, position = get_length_and_position(file, token_tuple, testset)
            res_filename = os.path.join(res_folder,
                                        file.replace('C:\\Users\\admin\\PycharmProjects\\ner_svm\\data\\devset\\',
                                                     '') + '.task1')
            with codecs.open(res_filename, 'a', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=' ')
                new_ne_tag = change_ne_name(dic_of_files_with_results[file][token_tuple])
                writer.writerow([new_ne_tag, position, length])

def change_ne_name(tag):
    if tag == 'Person':
        return 'PER'
    elif tag == 'Org':
        return 'ORG'
    elif tag == 'Location':
        return 'LOC'
    elif tag == 'LocOrg':
        return 'LOC'
    elif tag == 'Project':
        return 'ORG'
    else:
        raise ValueError('tag '+tag+" is not the right tag")


def get_length_and_position(file, token_tuple, test_set):
    position = test_set[file][token_tuple[0]][0]
    length = len(' '.join([test_set[file][token][2] for token in token_tuple]))
    return length, position
