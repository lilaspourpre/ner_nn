# -*- coding: utf-8 -*-
from src.enitites.tagged_token import TaggedToken


def get_tagged_tokens_from(dict_of_nes, token_tuple):
    """
    :param object_dict: dict of objects
    :param span_dict: dict of spans
    :param token_list: list of tokens
    :return: list of tagged tokens classes
    """
    list_of_tagged_tokens = ['O' for i in range(len(token_tuple))]

    for ne in dict_of_nes.values():
        for id in ne['tokens_list']:
            tag = format_tag(id, ne)
            id_in_token_tuple = [token.get_id() for token in token_tuple].index(id)
            token = token_tuple[id_in_token_tuple]
            list_of_tagged_tokens[id_in_token_tuple] = TaggedToken(tag, token)
    return list_of_tagged_tokens


def format_tag(id, ne):
    bilou = __choose_bilou_tag_for(id, ne['tokens_list'])
    formatted_tag = __tag_to_fact_ru_eval_format(ne['tag'])
    return bilou + formatted_tag


def __choose_bilou_tag_for(token_id, token_list):
    if len(token_list) == 1:
        return 'U'
    elif len(token_list) > 1:
        if token_list.index(token_id) == 0:
            return 'B'
        elif token_list.index(token_id) == len(token_list) - 1:
            return 'L'
        else:
            return 'I'


def __tag_to_fact_ru_eval_format(tag):
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
