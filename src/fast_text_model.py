# -*- coding: utf-8 -*-
from gensim.models.fasttext import FastText


def get_model_for_embeddings(documents):
    list_of_token_texts = []
    for document in documents:
        list_of_token_texts += document.get_sentences()
    model = FastText(sentences=list_of_token_texts, sg=1, size=200, alpha=0.025, window=5, min_count=5)
    return model
