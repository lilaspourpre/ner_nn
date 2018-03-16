# -*- coding: utf-8 -*-
import tensorflow as tf


class CNN():
    def __init__(self, input_size, output_size, hidden_size, batch_size):
        self.input_size = input_size
        self.output_size = output_size
        self.hidden_size = hidden_size

        self.batch_size = batch_size
        self.x = tf.placeholder(tf.float32, [None, None, self.input_size, 1], name='x')
        self.y = tf.placeholder(tf.float32, [None, None, self.output_size], name='y')
        self.seqlen = tf.placeholder(tf.int32, [None])

        self.conv1 = tf.layers.conv2d(inputs=self.x, filters=32, kernel_size=[5, 5], padding="same",
                                      activation=tf.nn.relu)
        self.pool1 = tf.layers.max_pooling2d(inputs=self.conv1, pool_size=[2, 2], strides=2)

        self.conv2 = tf.layers.conv2d(
            inputs=self.pool1,
            filters=64,
            kernel_size=[5, 5],
            padding="same",
            activation=tf.nn.relu)
        self.pool2 = tf.layers.max_pooling2d(inputs=self.conv2, pool_size=[2, 2], strides=2)
        self.pool2_flat = tf.reshape(self.pool2, [-1,])
        self.outputs = tf.contrib.layers.fully_connected(self.pool2_flat, self.output_size, activation_fn=None)
        #self.outputs = tf.contrib.layers.fully_connected(self.mid_outputs[-1], self.output_size, activation_fn=None)
        #dropout = tf.layers.dropout(inputs=dense, rate=0.4, training=mode == tf.estimator.ModeKeys.TRAIN)
        self.cross_entropy = tf.reduce_mean(
            tf.nn.softmax_cross_entropy_with_logits(logits=self.outputs,
                                                    labels=self.y))
        self.train = tf.train.AdamOptimizer(learning_rate=0.01).minimize(self.cross_entropy)

        self.init = tf.global_variables_initializer()
        self.sess = tf.Session()
        self.sess.run(self.init)
