# -*- coding: utf-8 -*-
import collections
import os
import codecs
import logging
from src.enitites.document import Document
from src.enitites.token import Token
from src.bilou import to_bilou


# ********************************************************************
#       Main function
# ********************************************************************

def get_documents_from(path):
    """
    Main function for getting documents
    :param path: path to the devset
    :return: dict of documents: {filename : DocumentClass}
    """
    dict_of_documents = {}
    filenames = __get_filenames_from(path)
    for filename in filenames:
        document = __create_document_from(filename)
        dict_of_documents[filename] = document
    return dict_of_documents


# -------------------------------------------------------------------
#       Getting filenames
# -------------------------------------------------------------------

def __get_filenames_from(path):
    """
    :param path: path ro devset
    :return: list of paths for each book without the extention
    """
    list_of_filenames = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.txt'):
                list_of_filenames.append(os.path.join(root, os.path.splitext(file)[0]))  # XXX splitext
    logging.log(logging.INFO, "Successfully got filenames from path")
    return list_of_filenames


# -------------------------------------------------------------------
#       Getting documents
# -------------------------------------------------------------------

def __create_document_from(filename):
    """
    :param filename: which document to parse (name without extension)
    :return: document class
    """
    tokens = __get_tokens_from(filename)
    tagged_tokens = __get_tagged_tokens_from(filename, tokens)
    document = Document(tagged_tokens)
    logging.log(logging.INFO, "SUCCESSFULLY CREATED: document for " + filename)
    return document


#
#       Getting tokens
#

def __get_tokens_from(filename):
    """
    :param filename: filename without extension (.tokens) to parse
    :return: list of token classes
    """
    tokens = []
    rows = __parse_file(filename + '.tokens')
    for row in rows:
        token = __create_token_from(row)
        tokens.append(token)
    return tuple(tokens)


def __parse_file(filename):
    """
    :param filename:
    :return: list of row lists
    """
    rows_to_return = []
    with codecs.open(filename, 'r', encoding='utf-8') as f:
        rows = f.read().split('\n')
    for row in rows:
        if len(row) != 0:
            rows_to_return.append(row.split(' # ')[0].split())
    return rows_to_return


def __create_token_from(row):
    """
    :param row: row that will be added to token class
    :return: token class
    """
    token = Token(tokenid=row[0], position=row[1], length=row[2], text=row[3])
    return token


#
#       Getting tagged tokens
#

def __get_tagged_tokens_from(filename, tokens):
    """
    :param filename: filename without extension (.spans and .objects) to parse
    :param tokens: tokens that need to be tagged
    :return: list of tagged tokens classes
    """
    span_dict = __spanid_to_tokenids(filename + '.spans',
                                     [token.get_id() for token in tokens])  # XXX span_to_tokens or spanid_to_tokenids
    object_dict = __to_dict_of_objects(filename + '.objects')
    dict_of_nes = __merge(object_dict, span_dict, [token.get_id() for token in tokens])
    return to_bilou.get_tagged_tokens_from(dict_of_nes, tokens)


# ___________________________________________________________________________________
#       Getting spans
#

def __spanid_to_tokenids(spanfile, token_ids):
    """
    :param spanfile: file that is going to be parsed
    :param token_ids:
    :return:
    """
    span_list = __parse_file(spanfile)
    dict_of_spans = {}
    for span in span_list:
        span_id = span[0]
        span_start = span[4]
        span_length_in_tokens = int(span[5])
        list_of_token_of_spans = __find_tokens_for(span_start, span_length_in_tokens, token_ids)

        dict_of_spans[span_id] = list_of_token_of_spans
    return dict_of_spans


def __find_tokens_for(start, length, token_ids):
    """
    :param start: first token in span
    :param length: number of tokens in span
    :param token_ids: list of all tokens in document
    :return: tokens that map the span
    """
    list_of_tokens = []
    index = token_ids.index(start)
    for i in range(length):
        list_of_tokens.append(token_ids[index + i])
    return list_of_tokens


# ___________________________________________________________________________________
#
#       Getting objects
#

def __to_dict_of_objects(object_file):
    """
    :param object_file: file that is goingto be parsed
    :return: dict of objects
    """
    object_list = __parse_file(object_file)
    dict_of_objects = {}
    for object in object_list:
        object_id = object[0]
        object_tag = object[1]
        object_spans = object[2:]
        dict_of_objects[object_id] = {'tag': object_tag, 'spans': object_spans}
    return dict_of_objects


# ___________________________________________________________________________________
#
#       Merge
#

def __merge(object_dict, span_dict, tokens):
    """
    :param object_dict:
    :param span_dict:
    :return:
    """
    ne_dict = __get_dict_of_nes(object_dict, span_dict)
    return __clean(ne_dict, tokens)


# ___________________________________________________________________________________

def __get_dict_of_nes(object_dict, span_dict):
    """
    :param object_dict:
    :param span_dict:
    :return:
    """
    ne_dict = collections.defaultdict(list)

    for object in object_dict.items():
        for span in span_dict.items():
            if span[0] in object[1]['spans']:
                ne_dict[(object[0], object[1]['tag'])].extend(span[1])
    for ne in ne_dict:
        ne_dict[ne] = sorted(list(set([int(i) for i in ne_dict[ne]])))
    return ne_dict


# ___________________________________________________________________________________

def __clean(ne_dict, tokens):
    """
    :param ne_dict:
    :param tokenslist:
    :return:
    """
    sorted_nes = sorted(ne_dict.items(), key=__sort_by_tokens)
    start_ne = sorted_nes[0]
    result_nes = {}
    for ne in sorted_nes:
        if __intersect(start_ne[1], ne[1]):
            result_nes[start_ne[0][0]] = {'tokens_list': __check_order([str(i) for i in start_ne[1]], tokens),
                                          'tag': start_ne[0][1]}
            start_ne = ne
        else:
            result_tokens_list = __check_normal_form(start_ne[1], ne[1])
            start_ne = (start_ne[0], result_tokens_list)
    return result_nes


def __sort_by_tokens(tokens):
    ids_as_int = [int(id) for id in tokens[1]]
    return (min(ids_as_int), -max(ids_as_int))


def __intersect(start_ne, current_ne):
    intersection = set.intersection(set(start_ne), set(current_ne))
    return intersection == set()


def __check_order(list_of_tokens, all_tokens):
    result = []
    for token in list_of_tokens:
        if token in all_tokens:
            result.append((token, all_tokens.index(token)))
    result = sorted(result, key=__sort_by_id)
    return [r[0] for r in result]


def __sort_by_id(result_tuple):
    return result_tuple[1]


def __check_normal_form(start_ne, ne):
    all_tokens = sorted(set.union(set(start_ne), set(ne)))
    return list(range(int(all_tokens[0]), int(all_tokens[-1]) + 1))
