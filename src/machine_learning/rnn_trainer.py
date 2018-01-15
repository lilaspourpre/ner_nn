# -*- coding: utf-8 -*-
from enitites.models.rnn_model import RNNModel
from machine_learning.i_model_trainer import ModelTrainer
from wrapper import complement_data, format_data
import numpy as np


class RNNTrainer(ModelTrainer):
    def __init__(self, epoch, nn):
        super().__init__()
        self.epoch = epoch
        self.nn = nn

    def batch_train(self, tagged_vectors, division):
        vectors = [tagged_vector.get_vector() for tagged_vector in tagged_vectors]
        array_of_vectors = np.array(complement_data(format_data(vectors, division), self.nn.seq_max_len),
                                    dtype='float32')
        array_of_tags = np.array(complement_data(format_data(
            self.translator([tagged_vector.get_tag() for tagged_vector in tagged_vectors], self.nn.tags), division),
            self.nn.seq_max_len),
            dtype='float32')
        seqlen_list = [len(i) for i in vectors]
        print(array_of_vectors.shape)
        print(array_of_tags.shape)
        return self.run_nn(array_of_vectors, array_of_tags, seqlen_list, division)

    def run_nn(self, array_of_vectors, array_of_tags, seqlen_list, division):
        for m in range(self.epoch):
            k = int(len(array_of_vectors) / self.nn.batch_size) if len(array_of_vectors) % self.nn.batch_size == 0 \
                else int(len(array_of_vectors) / self.nn.batch_size) + 1
            step = 0
            for j in range(k):
                self.nn.sess.run(self.nn.train, {self.nn.x: array_of_vectors[step:step + self.nn.batch_size],
                                                 self.nn.y: array_of_tags[step:step + self.nn.batch_size],
                                                 self.nn.seqlen: seqlen_list[step:step + self.nn.batch_size],
                                                 })
                print(
                    "loss: %s" % (
                        self.nn.sess.run([self.nn.cross_entropy],
                                         {self.nn.x: array_of_vectors[step:step + self.nn.batch_size],
                                          self.nn.y: array_of_tags[step:step + self.nn.batch_size],
                                          self.nn.seqlen: seqlen_list[
                                                          step:step + self.nn.batch_size]})))

                step += self.nn.batch_size
        return RNNModel(self.nn.sess, self.nn.outputs, self.nn.x, self.nn.output_size, self.nn.seqlen,
                        self.nn.seq_max_len, self.nn.tags, division)
