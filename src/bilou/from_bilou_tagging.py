# -*- coding: utf-8 -*-
import codecs


class FROM_BILOU():
    def __init__(self):
        self.corpus = []

    def untag(self, all_tokens_rows, tags):
        for i in range(len(all_tokens_rows)):
            self.corpus.append(list(all_tokens_rows[i]) + [tags[i]])

    def writing_to_file(self, filename='testset.txt'):
        with codecs.open(filename, 'w', encoding='utf-8') as f:
            for token_params in self.corpus:
                f.write(" ".join(token_params) + '\n')