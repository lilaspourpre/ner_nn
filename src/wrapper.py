# -*- coding: utf-8 -*-
import numpy as np

def complement_data(x, seq_max_len):
    new_x = []
    print(x)

    for i in range(len(x)):
        li = [[0. for k in range(x[i].shape[1])] for m in range(seq_max_len-len(x[i]))]
        new_x.append(np.concatenate((np.array(x[i]), np.array(li)), axis=0)) if li!=[] else new_x.append(x[i])
    return new_x
