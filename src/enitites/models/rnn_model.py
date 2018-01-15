# -*- coding: utf-8 -*-
import numpy as np
import tensorflow as tf
from enitites.models.model import Model
from wrapper import complement_data, format_data


class RNNModel(Model):
    def __init__(self, session, outputs, x, output_size, seqlen, max_seq_len, tags, division):
        super().__init__()
        self.session = session
        self.x = x
        self.outputs = outputs
        self.output_size = output_size
        self.seqlen = seqlen
        self.max_seq_len = max_seq_len
        self.tags = tags
        self.division = division

    def batch_predict(self, list_of_vectors):
        array_of_vectors = np.array(complement_data(format_data(list_of_vectors, self.division), self.max_seq_len),
                                    dtype='float32')
        output_shape = tf.shape(self.outputs)
        prediction = tf.nn.softmax(tf.reshape(self.outputs, [-1, self.output_size]))
        self.prediction = tf.reshape(prediction, output_shape)
        correct_prediction = tf.argmax(self.prediction, 2)
        index_list = correct_prediction.eval(feed_dict={self.x: array_of_vectors,
                                                        self.seqlen: [len(i) for i in list_of_vectors]},
                                             session=self.session)
        return [self.tags[i] for i in index_list]

    def __repr__(self):
        return 'rnn_model'
