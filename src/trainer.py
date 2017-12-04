# -*- coding: utf-8 -*-
from reader import get_documents_with_tags_from
from vector_creator import create_list_of_tagged_vectors
import datetime
# ********************************************************************
#       Main function
# ********************************************************************

def train(model_trainer, feature, path="C:\\Users\\admin\\PycharmProjects\\ner_svm\\data\\devset"):
    """
    :param path: path to devset
    :param method: ML method
    :return: trained model
    """
    documents = get_documents_with_tags_from(path)
    print('Docs are here for training', datetime.datetime.now())
    list_of_tagged_vectors = create_list_of_tagged_vectors(documents, feature)
    print('Vectors are created', datetime.datetime.now())
    return model_trainer.train(list_of_tagged_vectors)

