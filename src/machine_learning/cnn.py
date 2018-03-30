# -*- coding: utf-8 -*-
import tensorflow as tf
from tensorflow.python.framework import ops
from tensorflow.python.ops import gen_nn_ops


class CNN():
    def __init__(self, input_size, output_size, hidden_size, batch_size, filter_sizes=(3, 4, 5), pooling_size=2):
        self.input_size = input_size
        self.output_size = output_size
        self.hidden_size = hidden_size
        self.batch_size = batch_size
        self.filter_sizes = filter_sizes
        self.pooling_size = pooling_size

        self.x = tf.placeholder(tf.float32, [None, None, self.input_size], name='x')
        self.x_new = tf.expand_dims(self.x, -1)
        self.y = tf.placeholder(tf.float32, [None, None, self.output_size], name='y')
        self.seqlen = tf.placeholder(tf.int32, [None])

        # def apply_conv(f_size, input_tensor, o_size):
        #     filter = tf.Variable(tf.random_normal([f_size, self.input_size, 1, o_size], stddev=0.1))
        #     conv_outputs = tf.nn.conv2d(input_tensor, filter, [1, 1, self.input_size, 1], 'SAME')
        #     max_pool_outputs = tf.nn.max_pool(conv_outputs, [1, self.pooling_size, 1, 1], [1, 1, 1, 1], 'SAME')
        #     return tf.squeeze(max_pool_outputs, [self.pooling_size])
        #
        # self.conv = None
        # for i in range(len(self.filter_sizes)):
        #     if i != len(self.filter_sizes - 1):
        #         self.conv = apply_conv(self.filter_sizes[i], self.conv, self.hidden_size)
        #     elif i == 0:
        #         self.conv = apply_conv(self.filter_sizes[i], self.x_new, self.input_size)
        #     else:
        #         self.conv = apply_conv(self.filter_sizes[i], self.conv, self.input_size)



        self.filter4 = tf.Variable(tf.random_normal([5, self.input_size, 1, self.input_size], stddev=0.1))
        self.conv_outputs4 = tf.nn.conv2d(self.x_new, self.filter4, [1, 1, self.input_size, 1], 'SAME')
        self.max_pool_outputs4 = tf.nn.max_pool(self.conv_outputs4, [1, 2, 1, 1], [1, 1, 1, 1], 'SAME')
        self.max_pool_outputs4 = tf.squeeze(self.max_pool_outputs4, [2])
        self.conv_new = tf.expand_dims(self.max_pool_outputs4, -1)

        self.filter1 = tf.Variable(tf.random_normal([3, self.input_size, 1, self.hidden_size], stddev=0.1))
        self.conv_outputs1 = tf.nn.conv2d(self.conv_new, self.filter1, [1, 1, self.input_size, 1], 'SAME')
        self.max_pool_outputs1 = tf.nn.max_pool(self.conv_outputs1, [1, 3, 1, 1], [1, 1, 1, 1], 'SAME')
        self.max_pool_outputs1 = tf.squeeze(self.max_pool_outputs1, [2])

        self.filter2 = tf.Variable(tf.random_normal([4, self.input_size, 1, self.hidden_size], stddev=0.1))
        self.conv_outputs2 = tf.nn.conv2d(self.conv_new, self.filter2, [1, 1, self.input_size, 1], 'SAME')
        self.max_pool_outputs2 = tf.nn.max_pool(self.conv_outputs2, [1, 4, 1, 1], [1, 1, 1, 1], 'SAME')
        self.max_pool_outputs2 = tf.squeeze(self.max_pool_outputs2, [2])

        self.filter3 = tf.Variable(tf.random_normal([5, self.input_size, 1, self.hidden_size], stddev=0.1))
        self.conv_outputs3 = tf.nn.conv2d(self.conv_new, self.filter3, [1, 1, self.input_size, 1], 'SAME')
        self.max_pool_outputs3 = tf.nn.max_pool(self.conv_outputs3, [1, 5, 1, 1], [1, 1, 1, 1], 'SAME')
        self.max_pool_outputs3 = tf.squeeze(self.max_pool_outputs3, [2])

        self.max_pool_outputs = tf.concat([self.max_pool_outputs1, self.max_pool_outputs2, self.max_pool_outputs3], -1)

        self.outputs = tf.contrib.layers.fully_connected(self.max_pool_outputs, self.output_size, activation_fn=tf.tanh)
        mask = tf.sequence_mask(
            self.seqlen,
            dtype=tf.float32)

        self.cross_entropy = tf.nn.softmax_cross_entropy_with_logits(logits=self.outputs, labels=self.y)
        self.loss = (tf.reduce_sum(self.cross_entropy * mask) / tf.cast(tf.reduce_sum(self.seqlen), tf.float32))
        self.train = tf.train.AdamOptimizer(learning_rate=0.01).minimize(self.loss)

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
