import numpy as np
import pandas as pd
import re

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


#find regular expression for the word
def get_regular(word, pos_let):
    list_of_letters = [re.escape(i) for i in pos_let]
    reg = ''
    if len(list_of_letters) != 0:
        w = "[" +"".join(list_of_letters) + "]"
    else:
        w = ''
    for e in word:
        if e.islower():
            reg += w #choose a letter from possible variants
        else:
            reg += e.lower()
    reg += '$'
    return reg

def get_dataframe(subst, df, possible_letters, col_name):
    word = subst
    word_mask = get_regular(word, possible_letters)
    res = df[df[col_name].str.contains(word_mask, regex=True, na=False)]
    return res

def find_all_mask(diction, mask):
    r = re.compile(mask)
    newlist = list(filter(r.match, diction))
    return newlist

