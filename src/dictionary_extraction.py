# -*- coding: utf-8 -*-


class DictionaryBuilding:
    def __init__(self, spans=None, objects=None):
        self.__spans = spans
        self.__objects = objects
        self.__dic = {}

    def build_dict(self):
        for file in self.__objects.keys():
            current_objects = self.__objects[file]
            current_spans = self.__spans[file]
            for object in current_objects.keys():
                current_span_list = current_objects[object][1]
                current_tag = current_objects[object][0]
                current_len = len(current_span_list)
                for current_span in current_span_list:
                    for index in range(len(current_spans[current_span][5])):
                        self.__dic[current_spans[current_span][5][index]] = [object,
                                                                             current_spans[current_span][6][index],
                                                                             current_tag, current_len]

    def get_dic(self):
        self.build_dict()
        return self.__dic
