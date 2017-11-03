# -*- coding: utf-8 -*-
import logging
from src.reader import get_documents_from


def get_model(documents, method):
    pass
    # model = modelCreator()
    # return model.train_on(documents, method)


def train(method, path="C:\\Users\\admin\\PycharmProjects\\ner_svm\\data\\devset"):
    """
    :param path: path to devset
    :param method: ML method
    :return: trained model
    """
    logging.log(logging.INFO, "START OF Model Training")
    documents = get_documents_from(path)
    logging.log(logging.INFO, "SUCCESSFULLY CREATED: list of document classes")
    exit(0)
    model = get_model(documents, method)
    return model
