# -*- coding: utf-8 -*-
import logging
from src.enitites.tagged_vector import TaggedVector


# ********************************************************************
#       Main functions
# ********************************************************************

def create_list_of_tagged_vectors(documents, feature):
    """
    :param documents:
    :param feature:
    :return:
    """
    list_of_tagged_vectors = []

    for document in documents.values():
        lists_of_tokens = document.get_tokens()
        for taggedtoken in document.get_tagged_tokens():
            list_of_tagged_vectors.append(__create_tagged_vector_for(taggedtoken, lists_of_tokens, feature))
    return list_of_tagged_vectors


# ********************************************************************

def create_dict_of_vectors_for_each_doc(documents, feature):
    """
    :param documents:
    :param feature:
    :return:
    """
    list_of_tagged_vectors_for_each_doc = {}
    for document, document_values in documents.items():
        vectors_in_document = create_list_of_tagged_vectors({document:document_values}, feature)
        list_of_tagged_vectors_for_each_doc[document] = vectors_in_document
    return list_of_tagged_vectors_for_each_doc


# --------------------------------------------------------------------

def __create_tagged_vector_for(taggedtoken, tokenslist, feature):
    tag = taggedtoken.get_tag()
    vector = feature.compute_vector_for(taggedtoken.get_token(), tokenslist)
    return TaggedVector(vector=vector, tag=tag)


