# -*- coding: utf-8 -*-
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
    dict_of_nes = __merge(object_dict, span_dict)
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
    return list_of_tokens  # XXX not tuple, but list


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

def __merge(object_dict, span_dict):
    named_enities_dict = {}
    token_dict_with_object_ids = {}
    for object_id in object_dict:
        tag = object_dict[object_id]['tag']
        tokens_list = __get_all_tokens_for_spans(span_dict, object_dict[object_id]['spans'])

        for token in tokens_list:

            if token in token_dict_with_object_ids.keys():
                prev_token_list = named_enities_dict[token_dict_with_object_ids[token]]['tokens_list']


                if len(tokens_list) >= len(prev_token_list):
                    named_enities_dict, token_dict_with_object_ids = __delete_previous_entity(named_enities_dict,
                                                                                              token_dict_with_object_ids,
                                                                                              token, prev_token_list)
                    token_dict_with_object_ids[token] = object_id

                elif len(tokens_list) == len(prev_token_list) and tag == \
                        named_enities_dict[token_dict_with_object_ids[token]]['tag']:
                    named_enities_dict, token_dict_with_object_ids = __delete_previous_entity(named_enities_dict,
                                                                                              token_dict_with_object_ids,
                                                                                              token, prev_token_list)

                    token_dict_with_object_ids[token] = object_id
                    named_enities_dict[object_id] = {'tag': tag,
                                                     'tokens_list':
                                                         sorted(list(set.union(set(tokens_list),set(prev_token_list))))}
                    break

                elif len(tokens_list) == len(prev_token_list) and tag != \
                        named_enities_dict[token_dict_with_object_ids[token]]['tag']:
                    print('Error in object intersection')
                    print(tokens_list)
                    print(named_enities_dict[token_dict_with_object_ids[token]]['tokens_list'])
                    raise ValueError
                else:
                    break
            else:
                token_dict_with_object_ids[token] = object_id

        else:
            named_enities_dict[object_id] = {'tag': tag, 'tokens_list': tokens_list}
    return named_enities_dict

def __delete_previous_entity(named_enities_dict, token_dict_with_object_ids, token, prev_token_list):
    named_enities_dict.pop(token_dict_with_object_ids[token])
    for t in prev_token_list:
        token_dict_with_object_ids.pop(t)
    return named_enities_dict, token_dict_with_object_ids

def __get_all_tokens_for_spans(span_dict, span_list):
    common_list = []
    for span in span_list:
        common_list.extend(span_dict[span])
    return sorted(list(set(common_list)))
