# -*- coding: utf-8 -*-
from src.enitites import tagged_token_class


def get_tagged_tokens_from(dict_of_nes, token_list):
    """
    :param object_dict: dict of objects
    :param span_dict: dict of spans
    :param token_list: list of tokens
    :return: list of tagged tokens classes
    """
    list_of_tagged_tokens = []
    for token in token_list:
        tagged_token = tagged_token_class.TaggedTokens()
        tagged_token.set_token(token)
        tag = find_token_tag(token, dict_of_nes)
        tagged_token.set_tag(tag)
        list_of_tagged_tokens.append(tagged_token)
    return list_of_tagged_tokens


def find_token_tag(token, dict_of_nes):
    """
    :param token:
    :param object_dict:
    :param span_dict:
    :return:
    """
    common_list = []
    for i in dict_of_nes.values():
        common_list.extend(i[1])
    if token.get_id() not in common_list:
        return 'O'
    else:
        for tag, token_list in dict_of_nes.values():
            if token.get_id() in token_list:
                tag = tag_to_fact_ru_eval_format(tag)
                bilou_tag = choose_bilou_tag_for(token.get_id(), token_list)
                return bilou_tag + tag


def choose_bilou_tag_for(token_id, token_list):
    if len(token_list) == 1:
        return 'U'
    elif len(token_list) > 1:
        if token_list.index(token_id) == 0:
            return 'B'
        elif token_list.index(token_id) == len(token_list) - 1:
            return 'L'
        else:
            return 'I'


def tag_to_fact_ru_eval_format(tag):
    if tag == 'Person':
        return 'PER'
    elif tag == 'Org':
        return 'ORG'
    elif tag == 'Location':
        return 'LOC'
    elif tag == 'LocOrg':
        return 'LOC'
    elif tag == 'Project':
        return 'ORG'
    else:
        raise ValueError('tag ' + tag + " is not the right tag")
