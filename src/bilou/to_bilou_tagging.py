# -*- coding: utf-8 -*-
import codecs


class TO_BILOU():
    def __init__(self, dic):
        self.dic = dic
        self.corpus = []

    def tag(self, dataset):
        prev_bilou = None
        prev_ne_tag = None
        for id, token_text, position in dataset:
            if id in self.dic.keys():
                index = dataset.index((id, token_text, position))
                prev_token = dataset[index - 1]
                next_token = dataset[index + 1]
                # print(prev_token, id, token_text, position, next_token)
                # print(self.dic[id])
                # self.corpus.append([])
                # current_bilou = ''
                # current_ne_tag = ''
            else:
                self.corpus.append([id, token_text, position, 'O'])
        return self.corpus

    def writing_to_file(self, filename='trainset.txt'):
        with codecs.open(filename, 'w', encoding='utf-8') as f:
            for token_params in self.corpus:
                f.write(" ".join(token_params) + '\n')
