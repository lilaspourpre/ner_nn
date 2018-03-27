# -*- coding: utf-8 -*-
import tensorflow as tf
from tensorflow.python.framework import ops
from tensorflow.python.ops import gen_nn_ops


class CNN():
    def __init__(self, input_size, output_size, hidden_size, batch_size):
        self.input_size = input_size
        self.output_size = output_size
        self.hidden_size = hidden_size
        self.batch_size = batch_size

        self.x = tf.placeholder(tf.float32, [None, None, self.input_size], name='x')
        self.x_new = tf.expand_dims(self.x, -1)
        self.y = tf.placeholder(tf.float32, [None, None, self.output_size], name='y')
        self.seqlen = tf.placeholder(tf.int32, [None])

        self.filter = tf.Variable(tf.random_normal(5, self.input_size, 1, self.hidden_size], stddev = 0.1))
        self.conv_outputs = tf.nn.conv2d(self.x_new, self.filter, [1, 1, self.input_size, 1], 'SAME')
        self.max_pool_outputs = tf.nn.max_pool(self.conv_outputs, [1, 2, 1, 1], [1, 1, 1, 1], 'SAME')
        self.max_pool_outputs = tf.squeeze(self.max_pool_outputs, [2])
        # TODO:more filters, concat

        self.outputs = tf.contrib.layers.fully_connected(self.max_pool_outputs, self.output_size, activation_fn=None)
        #add mask
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
