# -*- coding: utf-8 -*-
import codecs, logging
import csv, os.path, datetime

def to_file(testset, dic_of_files_with_results, path=None):
    if path != None:
        if not os.path.exists(path):
            os.makedirs(path)
        res_folder = path
    else:
        folder = os.path.dirname(__file__)
        res_folder = folder.replace(os.path.basename(folder), 'result '+str(datetime.datetime.now().strftime(' %Y-%m-%d %H-%M-%S')))
        if not os.path.exists(res_folder):
            os.makedirs(res_folder)

    for file in dic_of_files_with_results.keys():
        logging.log(logging.INFO, 'Writing to ' + file)
        for token_tuple in dic_of_files_with_results[file].keys():
            length, position = get_length_and_position(file, token_tuple, testset)
            res_filename = os.path.join(res_folder, file.replace('C:\\Users\\admin\\PycharmProjects\\ner_svm\\data\\devset\\', '') + '.result')
            with codecs.open(res_filename, 'a', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=' ')
                writer.writerow([dic_of_files_with_results[file][token_tuple], length, position])

def get_length_and_position(file, token_tuple, test_set):
    position = test_set[file][token_tuple[0]][0]
    length = len(' '.join([test_set[file][token][2] for token in token_tuple]))
    return (length, position)