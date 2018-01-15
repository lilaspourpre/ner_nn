# -*- coding: utf-8 -*-
import tensorflow as tf
from tensorflow.contrib.layers.python.layers import initializers

class RNN():
    def __init__(self, input_size, tags, hidden_size, batch_size, seq_max_len):
        self.input_size = input_size
        self.tags = tags
        self.hidden_size = hidden_size
        self.seq_max_len = seq_max_len
        self.batch_size = batch_size
        self.x = tf.placeholder(tf.float32, [None, seq_max_len, self.input_size], name='x')
        self.y = tf.placeholder(tf.float32, [None, None, len(self.tags)], name='y')
        self.seqlen = tf.placeholder(tf.int32, [None])
        self.rnn_cell = tf.contrib.rnn.BasicLSTMCell(hidden_size)
        self.mid_outputs, state = tf.nn.dynamic_rnn(self.rnn_cell, self.x, sequence_length=self.seqlen,
                                                    swap_memory=True, dtype=tf.float32)
        self.outputs = self.create_layer(self.mid_outputs, len(self.tags), activation_fn=tf.nn.tanh)
        self.cross_entropy = tf.reduce_mean(
            tf.nn.softmax_cross_entropy_with_logits(logits=self.outputs,
                                                    labels=self.y))
        self.train = tf.train.AdamOptimizer(learning_rate=0.01).minimize(self.cross_entropy)

        self.init = tf.global_variables_initializer()
        self.sess = tf.Session()
        self.sess.run(self.init)

    def create_layer(self, inputs, num_outputs, activation_fn=tf.nn.relu,
                     weights_initializer=initializers.xavier_initializer(),
                     biases_initializer=tf.zeros_initializer()):
        W = tf.Variable(weights_initializer([inputs.shape[0].value, self.hidden_size, num_outputs]))
        b = tf.Variable(biases_initializer([num_outputs]))
        layer = activation_fn(tf.matmul(inputs, W) + b)
        return layer