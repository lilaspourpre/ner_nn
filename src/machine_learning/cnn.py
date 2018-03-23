# -*- coding: utf-8 -*-
import numpy
import tensorflow as tf
from tensorflow.python.framework import ops
from tensorflow.python.ops import gen_nn_ops


class CNN():
    def __init__(self, input_size, output_size, hidden_size, batch_size):
        self.input_size = input_size
        self.output_size = output_size
        self.hidden_size = hidden_size
        self.batch_size = batch_size

        self.x = tf.placeholder(tf.float32, [None, self.max_len, self.input_size, 1], name='x')
        self.y = tf.placeholder(tf.float32, [None, None, self.output_size], name='y')
        self.seqlen = tf.placeholder(tf.int32, [None])

        self.conv = tf.layers.conv2d(inputs=self.x, filters=32, kernel_size=[5, 5], padding="same",
                                      activation=tf.nn.relu)

        self.pool = tf.layers.max_pooling2d(self.conv, 2, 2)
        self.flat_pool = tf.contrib.layers.flatten(self.pool)

        self.outputs = tf.contrib.layers.fully_connected(self.flat_pool, self.output_size, activation_fn=None)
        #self.outputs = tf.layers.dropout(self.outputs, rate=0.4, training=tf.estimator.ModeKeys.TRAIN)
        #self.outputs = tf.contrib.layers.fully_connected(self.mid_outputs[-1], self.output_size, activation_fn=None)
        #dropout = tf.layers.dropout(inputs=dense, rate=0.4, training=mode == tf.estimator.ModeKeys.TRAIN)
        self.cross_entropy = tf.reduce_mean(
            tf.nn.softmax_cross_entropy_with_logits(logits=self.outputs,
                                                    labels=self.y))
        self.train = tf.train.AdamOptimizer(learning_rate=0.01).minimize(self.cross_entropy)

        self.init = tf.global_variables_initializer()
        self.sess = tf.Session()
        self.sess.run(self.init)

    # copied from nn_ops.max_pool and changed gen_nn_ops._max_pool into gen_nn_ops._max_pool_v2
    def max_pool(self, value, ksize, strides, padding, data_format="NHWC", name=None):
        """Performs the max pooling on the input.

        Args:
          value: A 4-D `Tensor` of the format specified by `data_format`.
          ksize: A 1-D int Tensor of 4 elements.  The size of the window for
            each dimension of the input tensor.
          strides: A 1-D int Tensor of 4 elements.  The stride of the sliding
            window for each dimension of the input tensor.
          padding: A string, either `'VALID'` or `'SAME'`. The padding algorithm.
            See the @{tf.nn.convolution$comment here}
          data_format: A string. 'NHWC', 'NCHW' and 'NCHW_VECT_C' are supported.
          name: Optional name for the operation.

        Returns:
          A `Tensor` of format specified by `data_format`.
          The max pooled output tensor.
        """
        with ops.name_scope(name, "MaxPool", [value]) as name:
            value = ops.convert_to_tensor(value, name="input")
            return gen_nn_ops._max_pool_v2(value,
                                              ksize=ksize,
                                              strides=strides,
                                              padding=padding,
                                              data_format=data_format,
                                              name=name)
