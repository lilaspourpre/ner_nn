# -*- coding: utf-8 -*-
import tensorflow as tf


class CNN():
    def __init__(self, input_size, output_size, hidden_size, batch_size, filter_sizes=(3, 4, 5), pooling_size=2):
        self.input_size = input_size
        self.output_size = output_size
        self.hidden_size = hidden_size
        self.batch_size = batch_size
        self.filter_sizes = filter_sizes

        self.x = tf.placeholder(tf.float32, [None, None, self.input_size], name='x')
        self.x_new = tf.expand_dims(self.x, -1)
        self.y = tf.placeholder(tf.float32, [None, None, self.output_size], name='y')
        self.seqlen = tf.placeholder(tf.int32, [None])

        def apply_conv(f_size, input_tensor, o_size):
            filter = tf.Variable(tf.random_normal([f_size, self.input_size, 1, o_size], stddev=0.1))
            conv_outputs = tf.nn.conv2d(input_tensor, filter, [1, 1, self.input_size, 1], 'SAME')
            max_pool_outputs = tf.nn.max_pool(conv_outputs, [1, f_size, 1, 1], [1, 1, 1, 1], 'SAME')
            return tf.squeeze(max_pool_outputs, [2])

        def apply_conv2(f_size, input_tensor, o_size):
            W = tf.Variable(tf.truncated_normal([f_size, self.input_size, 1, o_size], stddev=0.1), name="W")
            b = tf.Variable(tf.constant(0.1, shape=[o_size]), name="b")
            conv = tf.nn.conv2d(
                input_tensor,
                W,
                strides=[1, 1, self.input_size, 1],
                padding="SAME")

            # Apply nonlinearity
            h = tf.nn.relu(tf.nn.bias_add(conv, b), name="relu")
            # Max-pooling over the outputs
            pooled = tf.nn.max_pool(
                h,
                ksize=[1, f_size, 1, 1],
                strides=[1, 1, 1, 1],
                padding='SAME',
                name="pool")
            return tf.squeeze(pooled, [2])

        self.conv1 = apply_conv2(self.filter_sizes[-1], self.x_new, self.input_size)
        self.conv1_new = tf.expand_dims(self.conv1, -1)

        for i in range(len(self.filter_sizes)):
            if i == 0:
                self.conv2 = apply_conv2(self.filter_sizes[i], self.conv1_new, self.hidden_size)
            else:
                self.conv2 = tf.concat([self.conv2,
                                        apply_conv2(self.filter_sizes[i], self.conv1_new, self.hidden_size)], -1)

        self.outputs = tf.contrib.layers.fully_connected(self.conv2, self.output_size, activation_fn=tf.tanh)

        mask = tf.sequence_mask(
             self.seqlen,
             dtype=tf.float32)

        self.cross_entropy = tf.nn.softmax_cross_entropy_with_logits(logits=self.outputs, labels=self.y)
        self.loss = (tf.reduce_sum(self.cross_entropy * mask) / tf.cast(tf.reduce_sum(self.seqlen), tf.float32))


        self.train = tf.train.AdamOptimizer(learning_rate=0.001).minimize(self.loss)

        #global_step = tf.Variable(0, name="global_step", trainable=False)
        #optimizer = tf.train.AdamOptimizer(0.001)
        #grads_and_vars = optimizer.compute_gradients(self.loss)
        #self.train = optimizer.apply_gradients(grads_and_vars, global_step=global_step)

        # self.params = tf.trainable_variables()
        # self.gradients = tf.gradients(self.loss, self.params)
        # self.clipped_gradients, _ = tf.clip_by_global_norm(self.gradients, 1)
        #
        # self.optimizer = tf.train.AdamOptimizer(learning_rate=0.001)
        # self.train = self.optimizer.apply_gradients(zip(self.clipped_gradients, self.params))

        self.init = tf.global_variables_initializer()
        self.sess = tf.Session()
        self.sess.run(self.init)
