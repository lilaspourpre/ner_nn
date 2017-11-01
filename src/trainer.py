# -*- coding: utf-8 -*-
import logging
from src.reader import get_filenames_from
from src.reader import get_document_from


def get_documents_from(path):
    dict_of_documents = {}
    filenames = get_filenames_from(path)
    for filename in filenames:
        document = get_document_from(filename)
        dict_of_documents[filename] = document
    return dict_of_documents

def get_model(documents, method):
    pass
    # model = modelCreator()
    # return model.train_on(documents, method)

def trainer(method, path="C:\\Users\\admin\\PycharmProjects\\ner_svm\\data\\devset", ):
    """
    :param path: path to devset
    :param method: ML method
    :return: trained model
    """
    logging.log(logging.INFO, "START OF Model Training")
    documents = get_documents_from(path)
    logging.log(logging.INFO, "SUCCESSFULLY CREATED: list of document classes")
    exit(0)
    get_model(documents, method)
