# -*- coding: utf-8 -*-
import os
import codecs
import csv
from datetime import datetime

from src.bilou import from_bilou
from src.reader import get_documents_without_tags_from
from src.vector_creator import create_dict_of_vectors_for_each_doc


# ********************************************************************
#       Main function
# ********************************************************************

def compute_nes(testset_path, feature, model, output_path):
    """
    :param testset_path:
    :param feature:
    :param model:
    :return:
    """
    output_path = os.path.join(output_path, datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
    documents = get_documents_without_tags_from(testset_path)
    dict_of_docs_with_vectors = create_dict_of_vectors_for_each_doc(documents, feature)

    for document_name, untagged_vectors_list in dict_of_docs_with_vectors.items():
        list_of_vectors = [untagged_vector.get_vector() for untagged_vector in untagged_vectors_list]
        ne_list = __define_nes(model, list_of_vectors, documents[document_name].get_tokens())
        __write_to_file(ne_list, document_name, output_path)

    return output_path


# --------------------------------------------------------------------

def __define_nes(model, vectors_list, tokens):
    list_of_tags = []
    for vector in vectors_list:
        list_of_tags.append(model.predict(vector))
    return from_bilou.untag(list_of_tags=list_of_tags, list_of_tokens=tokens)


# --------------------------------------------------------------------

def __write_to_file(nes, filename, path):
    """
    :param nes:
    :param filename:
    :param path:
    :return:
    """
    if not os.path.exists(path):
        os.makedirs(path)

    for ne in nes:
        with codecs.open(os.path.join(path, os.path.basename(filename + ".task1")), 'a', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=' ')
            writer.writerow(ne)
