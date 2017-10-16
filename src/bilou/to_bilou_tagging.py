# -*- coding: utf-8 -*-
import codecs, logging


class TO_BILOU():
    def __init__(self, dic):
        self.dic = dic
        self.trainset = []

    def tag(self, dataset):
        for file in dataset.keys():
            for token in dataset[file].keys():
                for token_id, token_text, position in dataset[file][token]:
                    if token_id in self.dic.keys():
                        cur_object_id = self.dic[token_id][0]
                        cur_common_tag = self.dic[token_id][2]

                        prev_token_id = str(int(token_id) - 1)
                        prev_object_id = None

                        next_token_id = str(int(token_id) + 1)
                        next_object_id = None

                        if prev_token_id in self.dic.keys():
                            prev_object_id = self.dic[prev_token_id][0]

                        if next_token_id in self.dic.keys():
                            next_object_id = self.dic[next_token_id][0]

                        if prev_object_id is not None and next_object_id is not None:  # если токены (след. и пред.) тоже из словаря NE
                            if prev_object_id == cur_object_id and cur_object_id == next_object_id:
                                self.trainset.append([token_id, token_text, position, 'I' + cur_common_tag])
                            else:
                                if prev_object_id == cur_object_id:
                                    self.trainset.append([token_id, token_text, position, 'L' + cur_common_tag])
                                elif next_object_id == cur_object_id:
                                    self.trainset.append([token_id, token_text, position, 'B' + cur_common_tag])
                                else:
                                    self.trainset.append([token_id, token_text, position, 'U' + cur_common_tag])
                                pass

                        elif prev_object_id is None and next_object_id is not None:  # если нет предыдущего в словаре, а только этот и следующий, то проверять, один ли это объект
                            if cur_object_id == next_object_id:  # если это один объект, то это начало B
                                self.trainset.append([token_id, token_text, position, 'B' + cur_common_tag])
                            else:  # если разные, то это разные объекты
                                self.trainset.append([token_id, token_text, position, 'U' + cur_common_tag])

                        elif prev_object_id is not None and next_object_id is None:
                            if cur_object_id == prev_object_id:  # если это один объект, то это начало B
                                self.trainset.append([token_id, token_text, position, 'L' + cur_common_tag])
                            else:  # если разные, то это разные объекты
                                self.trainset.append([token_id, token_text, position, 'U' + cur_common_tag])

                        elif prev_object_id is None and next_object_id is None:
                            self.trainset.append([token_id, token_text, position, 'U' + cur_common_tag])

                        else:
                            logging.log(logging.ERROR, "BILOU to_tag doesn't work properly")
                    else:
                        self.trainset.append([token_id, token_text, position, 'O'])
        return self.trainset

    def writing_to_file(self, filename='trainset.txt'):
        with codecs.open(filename, 'w', encoding='utf-8') as f:
            for token_params in self.trainset:
                f.write(" ".join(token_params) + '\n')
