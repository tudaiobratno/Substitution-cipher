import numpy as np
import pandas as pd

def replace_dots(s):
    words = s.replace('.', '')
    words = words.replace(',', '')
    words = words.replace('!', '')
    words = words.replace('?', '')
    words = words.replace('«', '')
    words = words.replace('»', '')
    return words

def get_type(s):
    temp = list(s)
    used = {}
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


file_rus = open('words.txt', 'r')
list_of_words = []
for line in file_rus:
    list_of_words.append((line.rstrip().lower()))

dict_of_types = dict()
dict_of_len = dict()

for elem in list_of_words:
    result = get_type(elem)

    if result not in dict_of_types:
        dict_of_types[result] = [elem]
    else:
        dict_of_types[result].append(elem)

    t = len(elem)

    if t not in dict_of_len:
        dict_of_len[t] = [elem]
    else:
        dict_of_len[t].append(elem)




