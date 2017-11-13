# -*- coding: utf-8 -*-
import logging
from src.enitites.tagged_vector import TaggedVector
from src.enitites.features.composite import FeatureComposite


# ********************************************************************
#       Main function
# ********************************************************************

# XXX it's not feature_list - its a feature. Bad code below is probably caused by misunderstanding of it.
# XXX It can be written much simpler
def create_list_of_tagged_vectors(documents, feature_list):
    list_of_tagged_vectors = []
    if feature_list.get_feature_list_length() is None: # XXX this looks like "if False:" 
        logging.log(logging.INFO, "NO VECTORS WILL BE CREATED")
        for document in documents:
            list_of_tagged_vectors.extend([TaggedVector(vector=[], tag=taggedtoken.get_tag())
                                           for taggedtoken in documents[document].get_tagged_tokens()])
    else:
        logging.log(logging.INFO, "START of creating vectors")
        logging.log(logging.INFO, "*************************")
        for document in documents: # XXX consider using documents.values()
            document_list_with_tokens = create_document_with_tokens(documents[document])
            list_of_tagged_vectors.extend([__create_tagged_vector_for(taggedtoken, document_list_with_tokens, feature_list)
                                           for taggedtoken in documents[document].get_tagged_tokens()])
            logging.log(logging.INFO, "CREATED: vectors for document: "+document)
        logging.log(logging.INFO, "*************************")
    return list_of_tagged_vectors

# XXX this looks like Document's method get_tokens()
def create_document_with_tokens(document):
    document_list_with_tokens = []
    for tagged_token in document.get_tagged_tokens():
        document_list_with_tokens.append(tagged_token.get_token())
    return document_list_with_tokens


def __create_tagged_vector_for(taggedtoken, document, feature_composite):
    tag = taggedtoken.get_tag()
    vector = feature_composite.compute_vector_for(taggedtoken.get_token(), document)
    return TaggedVector(vector=vector, tag=tag)
