# -*- coding: utf-8 -*-
import numpy as np
import tensorflow as tf
from enitites.models.model import Model

class MultilayerPerceptronModel(Model):
    def __init__(self, session, model, x, tags):
        super().__init__()
        self.session = session
        self.x = x
        self.model = model
        self.tags = tags

    def predict(self, vector):
        array_of_vectors = np.array([vector], dtype='float32')
        prediction = tf.argmax(self.model)
        index = prediction.eval(feed_dict={self.x: array_of_vectors}, session=self.session)
        print(index)
        print(type(index))
        exit(0)
        return self.tags[int(index)]

    def __repr__(self):
        return 'mlperc_model'
