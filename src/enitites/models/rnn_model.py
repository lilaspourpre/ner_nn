# -*- coding: utf-8 -*-
import numpy as np
import tensorflow as tf
from enitites.models.model import Model
from wrapper import complement_data, format_data


class RNNModel(Model):
    def __init__(self, session, outputs, x, seqlen, max_seq_len, tags):
        super().__init__()
        self.session = session
        self.x = x
        self.outputs = outputs
        self.seqlen = seqlen
        self.max_seq_len = max_seq_len
        self.tags = tags

    def split_batch_predict(self, list_of_vectors, division):
        splitted_vectors, seqlen_list = format_data(list_of_vectors, division)
        array_of_vectors = np.array(complement_data(splitted_vectors, self.max_seq_len),
                                    dtype='float32')
        #output_shape = tf.shape(self.outputs)
        #prediction = tf.nn.softmax(tf.reshape(self.outputs, [-1, len(self.tags)]))
        #prediction_ = tf.reshape(prediction, output_shape)
        #correct_prediction = tf.argmax(prediction_, 2)
        correct_prediction = tf.argmax(self.outputs, 2)
        
        #output___ = prediction_.eval(feed_dict={self.x: array_of_vectors,
        #                                                self.seqlen: seqlen_list},
        #                                    session=self.session)
        #correct_prediction = tf.argmax(self.outputs, 2)
        index_list, output___ = self.session.run([correct_prediction, self.outputs],
                                                 feed_dict={self.x: array_of_vectors,
                                                        self.seqlen: seqlen_list})
        
        #
        #index_list = correct_prediction.eval(feed_dict={self.x: array_of_vectors,
        #                                                self.seqlen: seqlen_list},
        #
        #                                     session=self.session)
        print(index_list.shape)
        for i in range(len(index_list)):
            #print([self.tags[list_of_vectors[i][j]] for j in range(splitted_vectors[i])])
            pass
        #exit(0)
        result = []
        for j in range(len(index_list)):
            predicted_tags = index_list[j]
            for i in range(seqlen_list[j]):
                result.append(self.tags[predicted_tags[i]])
        return result
        
        #return [self.tags[list_of_vectors[i][j]] for j in range(splitted_vectors[i])]

    def __repr__(self):
        return 'rnn_model'
