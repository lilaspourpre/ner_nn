# -*- coding: utf-8 -*-
import numpy as np

def complement_data(x, seq_max_len):
    print(len(x[0]))
    print(x[0])
    print(len(x[0][0]))
    print(x[0][0])
    print(np.array(x).shape)
    exit(0)
    new_x = []
    for i in range(len(x)):
        li = [[0. for k in range(x[i].shape[1])] for m in range(seq_max_len-len(x[i]))]
        new_x.append(np.concatenate((np.array(x[i]), np.array(li)), axis=0)) if li!=[] else new_x.append(x[i])
    return new_x

def format_data(list_of_vectors, division):
    splitted_vectors = [[list_of_vectors.pop(0) for i in range(step)] for step in division]
    return splitted_vectors