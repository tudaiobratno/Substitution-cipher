import numpy as np

def prepare_str(s):
    list_of_symbols = list(s)
    to_lower = lambda x: x.lower()
    vfunc = np.vectorize(to_lower)
    lowered_symb = vfunc(list_of_symbols)
    lowered_symb = ''.join(lowered_symb.tolist())

    return lowered_symb


def freq(s):
    f = np.unique(np.array(list(s)), return_counts=True)
    d = dict()
    names, nums = f[0], f[1]
    for i in range(len(names)):
        d[names[i]] = nums[i]

    return d