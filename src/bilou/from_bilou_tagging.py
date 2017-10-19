# -*- coding: utf-8 -*-
import codecs
import logging


class FromBILOU:
    def __init__(self):
        self.dic_of_files_of_results = {}

    def untag(self, dict_of_data, dict_of_tags):
        for file in dict_of_data.keys():
            dic_of_results = {}
            ne_tokens = []
            prev_tag = None
            token_position_dic = {dict_of_data[file][key][0]: key for key in dict_of_data[file].keys()}
            for token_id in dict_of_data[file]:
                token_text = dict_of_data[file][token_id][2]
                position = dict_of_data[file][token_id][0]
                full_tag = dict_of_tags[file][token_id]

                cur_bilou_tag = full_tag[0:1]
                cur_common_tag = full_tag[1:]

                if cur_bilou_tag == 'U':  # если отдельный тег, то мы просто добавляем слово
                    dic_of_results[tuple([token_id])] = cur_common_tag

                elif cur_bilou_tag == 'B' or cur_bilou_tag == 'I':
                    dic_of_results, ne_tokens, prev_tag = self.tag_b_or_i_case(position, token_position_dic, file,
                                                                               dict_of_tags, cur_bilou_tag, ne_tokens,
                                                                               token_id, token_text, dic_of_results,
                                                                               prev_tag, cur_common_tag)

                elif cur_bilou_tag == 'L':
                    dic_of_results = self.tag_l_case(ne_tokens, token_id, cur_common_tag, dic_of_results)
                    ne_tokens = []
                    prev_tag = None

            if ne_tokens:
                dic_of_results[tuple(ne_tokens)] = prev_tag
            self.dic_of_files_of_results[file] = dic_of_results

        return self.dic_of_files_of_results


    def tag_b_or_i_case(self, position, token_position_dic, file, dict_of_tags, cur_bilou_tag, ne_tokens, token_id,
                        token_text, dic_of_results, prev_tag, cur_common_tag):
        if int(position) == max(list(map(lambda x: int(x), token_position_dic.keys()))):
            logging.log(logging.ERROR, 'somehow bilou tag B(/I) is the last tag in file ' + str(file))
        else:
            sorted_list = sorted(
                list(map(lambda x: int(x), token_position_dic.keys())))  # отсортированный список позиций
            next_index = sorted_list.index(int(position)) + 1  # находим индекс следующей позици
            next_position = sorted_list[next_index]
            next_token_id = token_position_dic[str(next_position)]
            next_bilou_tag = dict_of_tags[file][str(next_token_id)][0:1]
            next_common_tag = dict_of_tags[file][str(next_token_id)][1:]

            if cur_bilou_tag == 'B':  # если первый тег В
                dic_of_results, ne_tokens, prev_tag = self.tag_b_case(ne_tokens, dic_of_results, prev_tag,
                                                                      next_bilou_tag, next_common_tag, cur_common_tag,
                                                                      token_id, token_text)

            elif cur_bilou_tag == 'I':  # do we need to check some parameters? same type is already checked
                dic_of_results, ne_tokens, prev_tag = self.tag_i_case(next_bilou_tag, next_common_tag,
                                                                      cur_common_tag, ne_tokens, token_id,
                                                                      dic_of_results)

        return dic_of_results, ne_tokens, prev_tag


    def tag_b_case(self, ne_tokens, dic_of_results, prev_tag, next_bilou_tag, next_common_tag, cur_common_tag,
                   token_id, token_text):
        if ne_tokens:  # если у нас что-то осталось вne_tokens
            dic_of_results[tuple(ne_tokens)] = prev_tag  # то мы это добавляем
            ne_tokens = []  # и ощищаем временное хранилище
            prev_tag = None
            if (next_bilou_tag == 'I' or next_bilou_tag == 'L') and next_common_tag == cur_common_tag:
                prev_tag = cur_common_tag
                ne_tokens.append(token_id)
            else:
                logging.log(logging.ERROR,
                            'after B (' + token_id + " " + token_text +
                            ') is not I and L (or I/L of another class)')
                dic_of_results[tuple([token_id])] = cur_common_tag
        return dic_of_results, ne_tokens, prev_tag

    def tag_i_case(self, next_bilou_tag, next_common_tag, cur_common_tag, ne_tokens, token_id, dic_of_results):
        if (next_bilou_tag == 'I' or next_bilou_tag == 'L') and next_common_tag == cur_common_tag:
            prev_tag = cur_common_tag
            ne_tokens.append(token_id)
        else:
            ne_tokens.append(token_id)
            dic_of_results[tuple(ne_tokens)] = cur_common_tag
            ne_tokens = []
            prev_tag = None
        return dic_of_results, ne_tokens, prev_tag

    def tag_l_case(self, ne_tokens, token_id, cur_common_tag, dic_of_results):
        ne_tokens.append(token_id)
        dic_of_results[tuple(ne_tokens)] = cur_common_tag
        return dic_of_results

    def writing_to_file(self, filename='testset.txt'):
        with codecs.open(filename, 'w', encoding='utf-8') as f:
            pass
            for file in self.dic_of_files_of_results.keys():
                f.write(file + '\n')
                for token in self.dic_of_files_of_results[file]:
                    f.write(str(list(token)) + ' ' + self.dic_of_files_of_results[file][token] + '\n')
