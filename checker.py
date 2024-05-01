from work_with_dictionary import dict_of_len, dict_of_types, get_type, list_of_words, replace_dots
from mask import find_all_mask, find_regular2



def check(dict, s, USED):
    list_w = replace_dots(s).split(' ')
    rrr = []
    q = []
    for elem in list_w:
        if elem.lower() != find_regular2(elem, USED).rstrip('$'):
            o = find_all_mask(dict, find_regular2(elem, USED))
            rrr.append((len(o), -len(elem), o, elem))
            q.append(o)
    rrr = sorted(rrr)

    if [] in q:
        return ["ERROR"]
    else:
        return rrr
