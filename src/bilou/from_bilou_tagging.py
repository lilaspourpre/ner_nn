# -*- coding: utf-8 -*-
import codecs
import logging


class FROM_BILOU():
    def __init__(self):
        self.corpus = []
        self.dic_of_results = {}

    def untag(self, all_tokens_rows, tags):
        for i in range(len(all_tokens_rows)):
            self.corpus.append(list(all_tokens_rows[i]) + [tags[i]]) #now we have a corpus like in "to_bilou_tagging" output

        ne_tokens = []
        prev_tag = None

        for token_id, token_text, position, full_tag in self.corpus:
            index = self.corpus.index([token_id, token_text, position, full_tag])
            cur_bilou_tag = full_tag[0:1]
            cur_common_tag = full_tag[1:]

            if cur_bilou_tag == 'U':
                self.dic_of_results[zip([token_id])] = cur_common_tag

            elif cur_bilou_tag == 'B':

                if ne_tokens != []:
                    self.dic_of_results[zip(ne_tokens)] = prev_tag
                    ne_tokens = []

                if index == len(self.corpus)-1:
                    logging.log(logging.ERROR, 'somehow bilou tag B is the last tag in whole corpus')
                else:
                    next_bilou_tag = self.corpus[index + 1][3][0:1]
                    next_common_tag = self.corpus[index + 1][3][1:]

                    if (next_bilou_tag == 'I' or next_bilou_tag == 'L') and next_common_tag == cur_common_tag:
                        prev_tag = cur_common_tag
                        ne_tokens.append(token_id)

            elif cur_bilou_tag == 'I':
                ne_tokens.append(token_id)

            elif cur_bilou_tag == 'L':
                ne_tokens.append(token_id)
                self.dic_of_results[zip(ne_tokens)] = cur_common_tag
                ne_tokens = []
                prev_tag = None

        if ne_tokens != []:
            self.dic_of_results[zip(ne_tokens)] = prev_tag
        return self.dic_of_results

    def writing_to_file(self, filename='testset.txt'):
        with codecs.open(filename, 'w', encoding='utf-8') as f:
            for token_params in self.corpus:
                f.write(" ".join(token_params) + '\n')