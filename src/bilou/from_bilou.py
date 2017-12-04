# -*- coding: utf-8 -*-

def untag2(list_of_tags, list_of_tokens):
    """
    :param list_of_tags:
    :param list_of_tokens:
    :return:
    """
    if len(list_of_tags) == len(list_of_tokens):
        dict_of_final_ne = {}
        ne_words = []
        ne_tag = None

        for index in range(len(list_of_tokens)):
            current_tag = list_of_tags[index]
            current_token = list_of_tokens[index]

            if ne_tag == None and ne_words == []:
                if current_tag.startswith('U'):
                    dict_of_final_ne[tuple([current_token])] = current_tag[1:]
                elif not current_tag.startswith('O'):
                        ne_tag = current_tag[1:]
                        ne_words.append(current_token)
            elif ne_tag is not None and ne_words != []:
                if 'O' == current_tag or current_tag.startswith('U'):
                    dict_of_final_ne[tuple(ne_words)] = ne_tag
                    ne_tag = None
                    ne_words = []
                    if current_tag.startswith('U'):
                        dict_of_final_ne[tuple([current_token])] = current_tag[1:]
                else:
                    if ne_tag == current_tag[1:]:
                        if current_tag.startswith('B'):
                            dict_of_final_ne[tuple(ne_words)] = ne_tag
                            ne_words = [current_token]
                        else:
                            ne_words.append(current_token)
                            if current_tag.startswith('L'):
                                dict_of_final_ne[tuple(ne_words)] = ne_tag
                                ne_tag = None
                                ne_words = []
                    else:
                        dict_of_final_ne[tuple(ne_words)] = ne_tag
                        ne_tag = current_tag[1:]
                        ne_words = [current_token]
            else:
                if ne_tag is None:
                    raise Exception('Somehow ne_tag is None and ne_words is not None')
                else:
                    raise Exception('Somehow ne_words is None and ne_tag is not None')

        return __to_output_format(dict_of_final_ne)
    else:
        raise ValueError('lengths are not equal')

def untag(list_of_tags, list_of_tokens):
    """
    :param list_of_tags:
    :param list_of_tokens:
    :return:
    """
    if len(list_of_tags) == len(list_of_tokens):
        dict_of_final_ne = {}
        ne_words = []
        ne_tag = None

        for index in range(len(list_of_tokens)):
            current_tag = list_of_tags[index]
            current_token = list_of_tokens[index]

            # XXX need to correctly deal with all 'possible' combinations.
            # XXX for now some of them are ignored: O O I..., O O L...
            if ne_tag == None and current_tag.startswith('U'):
                dict_of_final_ne[tuple([current_token])] = current_tag[1:]

            elif ne_tag == None and current_tag.startswith('B'):
                ne_tag = current_tag[1:]
                ne_words.append(current_token)

            # XXX more weird combinations: BPer BLoc,
            elif ne_tag is not None and 'O' != current_tag:
                ne_words.append(current_token)
                if ne_tag in current_tag and current_tag.startswith('L'):
                    dict_of_final_ne[tuple(ne_words)] = ne_tag
                    ne_tag = None
                    ne_words = []

            elif ne_tag is not None and 'O' == current_tag:
                dict_of_final_ne[tuple(ne_words)] = ne_tag
                ne_tag = None
                ne_words = []

        return __to_output_format(dict_of_final_ne)
    else:
        raise ValueError('lengths are not equal')



def __to_output_format(dict_nes):
    """
    :param dict_nes:
    :return:
    """
    list_of_results_for_output = []

    for tokens_tuple, tag in dict_nes.items():
        position = tokens_tuple[0].get_position()
        length = sum([len(token.get_text())+1 for token in tokens_tuple])-1
        list_of_results_for_output.append([tag, position, length])

    return list_of_results_for_output


def __to_output_format2(dict_nes):
    """
    :param dict_nes:
    :return:
    """
    list_of_results_for_output = []

    for tokens_tuple, tag in dict_nes.items():
        position = int(tokens_tuple[0].get_position())
        length = int(tokens_tuple[-1].get_position()) + len(tokens_tuple[-1].get_text()) - 1 - position
        list_of_results_for_output.append([tag, position, length])

    return list_of_results_for_output
