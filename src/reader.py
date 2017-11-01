# -*- coding: utf-8 -*-
import os
import codecs
import logging
from src.enitites import document_class
from src.enitites import token_class
from src.bilou import to_bilou


def get_filenames_from(path):
    """
    :param path: path ro devset
    :return: list of paths for each book without the extention
    """
    list_of_filenames = []
    for root, dirs, files in os.walk(path):
        for file in files:  # for each file in folder
            if file.endswith('.txt'):  # if it ends with .objects
                list_of_filenames.append(os.path.join(root, file[:-4]))  # we add it to the list of files
    logging.log(logging.INFO, "Successfully got filenames from path")
    return list_of_filenames


def get_document_from(filename):
    """
    :param filename: which document to parse (name without extension)
    :return: document class
    """
    tokens = get_tokens_from(filename)
    #logging.log(logging.INFO, "got_tokens_from "+filename)
    tagged_tokens = get_tagged_tokens_from(filename, tokens)
    #logging.log(logging.INFO, "got_tagged_tokens_from "+filename)
    document = document_class.Document(tagged_tokens)
    logging.log(logging.INFO, "SUCCESSFULLY CREATED: document for "+filename)
    return document


def get_tokens_from(filename):
    """
    :param filename: filename without extension (.tokens) to parse
    :return: list of token classes
    """
    tokens = []
    rows = parse_file(filename + '.tokens')
    for row in rows:
        token = set_token_from(row)
        tokens.append(token)
    return tokens


def get_tagged_tokens_from(filename, tokens):
    """
    :param filename: filename without extension (.spans and .objects) to parse
    :param tokens: tokens that need to be tagged
    :return: list of tagged tokens classes
    """
    span_list = parse_file(filename + '.spans')
    span_dict = to_dict_of_spans(span_list, [token.get_id() for token in tokens])
    object_list = parse_file(filename + '.objects')
    object_dict = to_dict_of_objects(object_list)
    dict_of_nes = merge(object_dict, span_dict)
    return to_bilou.get_tagged_tokens_from(dict_of_nes, tokens)

def merge(object_dict, span_dict):
    named_enities_dict = {}
    for object_id in object_dict:
        for tuple_object in object_dict[object_id]['true_objects']:
            tag = object_dict[object_id]['tag']
            tokens_list = get_all_tokens_for_spans(span_dict, tuple_object)
            named_enities_dict[tuple_object] = [tag, tokens_list]
    return named_enities_dict

def get_all_tokens_for_spans(span_dict, tuple_object):
    common_list = []
    for span in tuple_object:
        common_list.extend(span_dict[span]['token_list'])
    return list(set(common_list))

def to_dict_of_objects(object_list):
    """
    :param object_list: list of objects with parameters
    :return: dict of objects
    """
    dict_of_objects = {}
    for object in object_list:
        object_id = object[0]
        object_tag = object[1]
        object_spans = object[2:]
        true_objects = divide(object_spans)
        dict_of_objects[object_id] = {'tag':object_tag, 'spans':object_spans, 'true_objects':true_objects}
    return dict_of_objects

def divide(object_spans):
    """
    :param object_spans: spans in object may contain several objects that need to be divided
    :return: list of tuples of spans where tuple is a tuple of separate object
    """
    list_of_tuples_of_spans = []
    start_span = int(object_spans[0])
    start_index = 0
    for index in range(1, len(object_spans)):
        if start_span+index != int(object_spans[index]):
            list_of_tuples_of_spans.append(tuple(object_spans[start_index:index]))
            start_index = index
            start_span = int(object_spans[index])
    list_of_tuples_of_spans.append(tuple(object_spans[start_index:]))
    return list_of_tuples_of_spans

def to_dict_of_spans(span_list, token_ids):
    """
    :param span_list: list of spans with their parameters will be converted into dic
    :return: dict of spans (with list of all tokens)
    """
    dict_of_spans = {}
    for span in span_list:
        span_id = span[0]
        span_tag = span[1]
        span_position = span[2]
        span_length = span[3]
        span_start = span[4]
        span_length_in_tokens = span[5]

        list_of_token_of_spans = find_tokens_for(span_start, span_length_in_tokens, token_ids)

        dict_of_spans[span_id] = {'tag':span_tag, 'position':span_position, 'length':span_length, 'start':span_start,
                                  'length_in_tokens':span_length_in_tokens, 'token_list':list_of_token_of_spans}
    return dict_of_spans

def find_tokens_for(start, length, token_ids):
    """
    :param start: first token in span
    :param length: number of tokens in span
    :param token_ids: list of all tokens in document
    :return: tokens that map the span
    """
    list_of_tokens = []
    index = token_ids.index(start)
    for i in range(int(length)):
        list_of_tokens.append(token_ids[index+i])
    return list_of_tokens

def parse_file(filename):
    """
    :param filename:
    :return: list of row lists ['id','position','length','text']
    """
    rows_to_return = []
    with codecs.open(filename, 'r', encoding='utf-8') as f:
        rows = f.read().split('\n')
    for row in rows:
        if len(row) != 0:
            rows_to_return.append(row.split(' # ')[0].split())
    return rows_to_return


def set_token_from(row):
    """
    :param row: row ['id','position','length','text'] that will be added to token class
    :return: token class
    """
    try:
        token = token_class.Token(id=row[0], position=row[1], length=row[2], text=row[3])
        return token
    except IndexError as e:
        logging.log(logging.ERROR, " Something wrong with token row length")
        exit(1)
