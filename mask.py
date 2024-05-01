import re
from work_with_dictionary import dict_of_len, dict_of_types, get_type, list_of_words
def find_regular(s, L):
    reg = ''
    for e in s:
        if e.islower():
            reg += '.'
        else:
            reg += e.lower()
    reg += '$'
    return reg


def find_all_mask(diction, mask):
    r = re.compile(mask)
    newlist = list(filter(r.match, diction))
    return newlist

def find_regular2(s, L):
    x_list = [re.escape(i) for i in L]  # turn each user-defined character into a regex literal
    reg = ''
    w = "[" +"".join(x_list) + "]"
    for e in s:
        if e.islower():
            reg += w
        else:
            reg += e.lower()
    reg += '$'
    return reg

