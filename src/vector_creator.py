# -*- coding: utf-8 -*-
from src.enitites.tagged_vector import TaggedVector
from src.enitites.features.composite import FeatureComposite


# ********************************************************************
#       Main function
# ********************************************************************

def create_list_of_tagged_vectors(documents, feature_list):
    list_of_tagged_vectors = []
    if len(feature_list) == 0:
        for document in documents:
            list_of_tagged_vectors.extend([TaggedVector(vector=[], tag=taggedtoken.get_tag())
                                           for taggedtoken in documents[document].get_tagged_tokens()])
    else:
        for document in documents:
            list_of_tagged_vectors.extend([__create_tagged_vector_for(taggedtoken, feature_list)
                                           for taggedtoken in documents[document].get_tagged_tokens()])
    return list_of_tagged_vectors


def __create_tagged_vector_for(taggedtoken, feature_list):
    tag = taggedtoken.get_tag()
    composite = FeatureComposite(feature_list)
    vector = composite.compute_vector_for(taggedtoken.get_token())
    return TaggedVector(vector=vector, tag=tag)
