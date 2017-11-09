# -*- coding: utf-8 -*-
from src.enitites.tagged_vector import TaggedVector

# ********************************************************************
#       Main function
# ********************************************************************

def create_list_of_tagged_vectors(documents):
    list_of_tagged_vectors = []
    for document in documents:
        list_of_tagged_vectors.extend(__create_tagged_vectors_for_document(documents[document]))
    return list_of_tagged_vectors


def __create_tagged_vectors_for_document(document):
    list_of_tagged_vectors = []
    for taggedtoken in document.get_tagged_tokens():
        list_of_tagged_vectors.append(__create_tagged_vector_for(taggedtoken))
    return list_of_tagged_vectors


def __create_tagged_vector_for(taggedtoken):
    tag = taggedtoken.get_tag()
    vector = __compute_vector(taggedtoken.get_token())
    return TaggedVector(vector=vector, tag=tag)

def __compute_vector(token):
    return [1,0]