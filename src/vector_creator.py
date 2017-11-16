# -*- coding: utf-8 -*-
import logging
from src.enitites.tagged_vector import TaggedVector


# ********************************************************************
#       Main function
# ********************************************************************

def create_list_of_tagged_vectors(documents, feature):
    list_of_tagged_vectors = []

    for document in documents.values():
        lists_of_tokens = document.get_tokens()
        for taggedtoken in document.get_tagged_tokens():
            list_of_tagged_vectors.append(__create_tagged_vector_for(taggedtoken, lists_of_tokens, feature))
            logging.log(logging.INFO, "SUCCESSFULLY CREATED: vector")
    return list_of_tagged_vectors


# --------------------------------------------------------------------

def __create_tagged_vector_for(taggedtoken, tokenslist, feature):
    tag = taggedtoken.get_tag()
    vector = feature.compute_vector_for(taggedtoken.get_token(), tokenslist)
    return TaggedVector(vector=vector, tag=tag)
