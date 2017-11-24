# -*- coding: utf-8 -*-
import collections
import os
import codecs
from collections import OrderedDict
from src.enitites.document import Document
from src.enitites.tagged_token import TaggedToken
from src.enitites.token import Token
from src.bilou import to_bilou


# ********************************************************************
#       Main functions
# ********************************************************************


def get_documents_with_tags_from(path):
    get_tagged_tokens_from = __get_tagged_tokens_from
    return __get_documents_from(path, get_tagged_tokens_from)


def get_documents_without_tags_from(path):
    get_tagged_tokens_from = __get_not_tagged_tokens_from
    return __get_documents_from(path, get_tagged_tokens_from)



# -------------------------------------------------------------------
#       Common private function for getting documents
# -------------------------------------------------------------------

def __get_documents_from(path, get_tagged_tokens_from):
    """
    Main function for getting documents
    :param path: path to the devset
    :return: dict of documents: {filename : DocumentClass}
    """
    dict_of_documents = {}
    filenames = __get_filenames_from(path)
    for filename in filenames:
        document = __create_document_from(filename, get_tagged_tokens_from)
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
            if file.endswith('.tokens'):
                list_of_filenames.append(os.path.join(root, os.path.splitext(file)[0]))  # XXX splitext
    return list_of_filenames


# -------------------------------------------------------------------
#       Getting documents
# -------------------------------------------------------------------

def __create_document_from(filename, get_tagged_tokens_from):
    """
    :param filename: which document to parse (name without extension)
    :return: document class
    """
    tokens = __get_tokens_from(filename)
    tagged_tokens = get_tagged_tokens_from(filename, tokens)
    document = Document(tagged_tokens)
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
    span_dict = __spanid_to_tokenids(filename + '.spans',[token.get_id() for token in tokens])
    object_dict = __to_dict_of_objects(filename + '.objects')
    dict_of_nes = __merge(object_dict, span_dict, tokens)
    return to_bilou.get_tagged_tokens_from(dict_of_nes, tokens)


#
#       Getting not tagged tokens
#

def __get_not_tagged_tokens_from(filename, tokens):
    """
    :param filename:
    :param tokens:
    :return:
    """
    return [TaggedToken(None, tokens[i]) for i in range(len(tokens))]


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
    ne_dict = collections.defaultdict(set)
    for obj_id, obj_values in object_dict.items():
        for span in obj_values['spans']:
            ne_dict[(obj_id, obj_values['tag'])].update(span_dict[span])
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
    result_nes = {}
    if len(sorted_nes) != 0:
        start_ne = sorted_nes[0]
        for ne in sorted_nes:
            if __not_intersect(start_ne[1], ne[1]):
                result_nes[start_ne[0][0]] = {
                    'tokens_list': __check_order(start_ne[1], tokens),
                    'tag': start_ne[0][1]}
                start_ne = ne
            else:
                result_tokens_list = __check_normal_form(start_ne[1], ne[1])
                start_ne = (start_ne[0], result_tokens_list)
        result_nes[start_ne[0][0]] = {
            'tokens_list': __check_order(start_ne[1], tokens),
            'tag': start_ne[0][1]}
    return result_nes


def __sort_by_tokens(tokens):
    ids_as_int = [int(id) for id in tokens[1]]
    return (min(ids_as_int), -max(ids_as_int))


def __not_intersect(start_ne, current_ne):
    intersection = set.intersection(set(start_ne), set(current_ne))
    return intersection == set()


def __check_normal_form(start_ne, ne):
    all_tokens = set.union(set(start_ne), set(ne))
    return __find_all_range_of_tokens(all_tokens)


def __find_all_range_of_tokens(tokens):
    tokens = sorted(tokens)
    if (tokens[-1] - tokens[0] - len(tokens)) < 5:
        return list(range(tokens[0], tokens[-1] + 1))
    else:
        return tokens


def __check_order(list_of_tokens, all_tokens):
    """
    :param list_of_tokens:
    :param all_tokens:
    :return:
    """
    list_of_tokens = [str(i) for i in __find_all_range_of_tokens(list_of_tokens)]
    result = []
    dict_of_text_by_id = OrderedDict()
    for i in range(len(all_tokens)):
        dict_of_text_by_id[all_tokens[i].get_id()] = (all_tokens[i].get_text(), i)
    for token in list_of_tokens:
        try:
            index_in_all = dict_of_text_by_id[token][1]
            result.append((token, index_in_all))
        except KeyError:
            pass
    result = sorted(result, key=__sort_by_position)
    result = add_quotation_marks(result, dict_of_text_by_id)
    return [r[0] for r in result]


def add_quotation_marks(result, dict_of_text_by_id):
    """
    :param result:
    :param dict_of_text_by_id:
    :return:
    """
    result_tokens_texts = [dict_of_text_by_id[token[0]][0] for token in result]
    prev_id = [r[1] for r in result][0] - 1
    next_id = [r[1] for r in result][-1] + 1

    if prev_id >= 0 and list(dict_of_text_by_id.values())[prev_id][0] == '«' \
            and '»' in result_tokens_texts and '«' not in result_tokens_texts:
        result = [(list(dict_of_text_by_id.keys())[prev_id], prev_id)] + result

    if next_id < len(dict_of_text_by_id) and list(dict_of_text_by_id.values())[next_id][0] == '»' \
            and '«' in result_tokens_texts and '»' not in result_tokens_texts:
        result = result + [(list(dict_of_text_by_id.keys())[next_id], next_id)]

    return result


def __sort_by_position(result_tuple):
    return result_tuple[1]
