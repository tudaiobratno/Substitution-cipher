import numpy as np

def get_type(s):
    temp = list(s)
    used = dict()
    ind = 0
    res = ''
    for let in temp:
        if let == '-':
            res += '-'
        elif let not in used:
            used[let] = str(ind)
            res += str(ind) + '.'
            ind += 1
        else:
            res += (used[let]) + '.'

    res = res.rstrip('.')
    return res

get_type_vect = np.vectorize(get_type)