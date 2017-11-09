# -*- coding: utf-8 -*-
import logging
from src.reader import get_documents_from
from src.vector_creator import create_list_of_tagged_vectors


def train(model_trainer, path="C:\\Users\\admin\\PycharmProjects\\ner_svm\\data\\devset"):
    """
    :param path: path to devset
    :param method: ML method
    :return: trained model
    """
    logging.log(logging.INFO, "START OF Model Training")
    documents = get_documents_from(path)
    logging.log(logging.INFO, "SUCCESSFULLY CREATED: list of document classes")
    list_of_tagged_vectors = create_list_of_tagged_vectors(documents)
    return model_trainer.train(list_of_tagged_vectors)

