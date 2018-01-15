# -*- coding: utf-8 -*-
import numpy as np

def complement_data(x, seq_max_len):
    r_x = np.array(x)
    new_x = []
    for i in range(len(r_x)):
        li = [[0. for k in range(np.array(r_x[i]).shape[1])] for m in range(seq_max_len-len(r_x[i]))]
        new_x.append(np.concatenate((np.array(r_x[i]), np.array(li)), axis=0)) if li!=[] else new_x.append(r_x[i])
    return new_x

def format_data(list_of_vectors, division):
    splitted_vectors = [[list_of_vectors.pop(0) for i in range(step)] for step in division]
    return splitted_vectors