# -*- coding: utf-8 -*-
from enitites.models.rnn_model import RNNModel
from machine_learning.i_model_trainer import ModelTrainer
from wrapper import complement_data, format_data


class RNNTrainer(ModelTrainer):
    def __init__(self, epoch, nn, tags):
        super().__init__()
        self.epoch = epoch
        self.nn = nn
        self.tags = tags

    def batch_train(self, tagged_vectors, division):
        vectors = [tagged_vector.get_vector() for tagged_vector in tagged_vectors]
        splitted_vectors, seqlen_list = format_data(vectors, division)
        splitted_tags, _ = format_data(
            self.translator([tagged_vector.get_tag() for tagged_vector in tagged_vectors], self.nn.tags), division)
        return self.run_nn(splitted_vectors, splitted_tags, seqlen_list)

    def run_nn(self, array_of_vectors, array_of_tags, seqlen_list):
        for m in range(self.epoch):
            k = int(len(array_of_vectors) / self.nn.batch_size) if len(array_of_vectors) % self.nn.batch_size == 0 \
                else int(len(array_of_vectors) / self.nn.batch_size) + 1
            step = 0
            for j in range(k):
                array_x = complement_data(array_of_vectors[step:step + self.nn.batch_size])
                array_y = complement_data(array_of_tags[step:step + self.nn.batch_size])
                self.nn.sess.run(self.nn.train,
                                 {self.nn.x: array_x,
                                  self.nn.y: array_y,
                                  self.nn.seqlen: seqlen_list[step:step + self.nn.batch_size],
                                  })
                print("loss: %s %s %s" % (self.nn.sess.run([self.nn.cross_entropy],
                                                     {self.nn.x: array_x, self.nn.y: array_y,
                                                      self.nn.seqlen: seqlen_list[step:step + self.nn.batch_size]}),m,j))
                step += self.nn.batch_size
        return RNNModel(self.nn.sess, self.nn.outputs, self.nn.x, self.nn.seqlen, self.tags)
