from work_with_dictionary import dict_of_len, dict_of_types, get_type, list_of_words, replace_dots
from frequency import freq, prepare_str
from mask import find_all_mask, find_regular2
from checker import check

table = [[1 for i in range(33)] for i in range(33)]
plain_text="We visited many famous tourist places. My favorite was the Louvre, a well-known museum. I was always interested in art, so that was a special treat for me."
USED = [chr(ord('a') + i) for i in range(26)]
cipher_text = plain_text

#freq analysis
prepared_cipher_text = prepare_str(cipher_text)
list_of_freq = freq(prepared_cipher_text)


#find words
words = replace_dots(prepared_cipher_text)
words = words.split(' ')
words = sorted(words, key=len, reverse=True)

#Find rare words

types_of_words = []
len_of_words = []

for elem in words:
    cur_type = get_type(elem)
    types_of_words.append((len(dict_of_types[cur_type]), elem, cur_type))
    len_of_words.append((len(elem), elem))

len_of_words = sorted(len_of_words)
tup = sorted(types_of_words)

#find rare words
i = tup[0][0]
ind = 0
probably = []
print(tup)
while i < 10:
    print(f"Вероятно, слово {tup[ind][1]} является одним из: {dict_of_types[tup[ind][2]]}")
    probably.append((tup[ind][1], dict_of_types[tup[ind][2]]))
    ind += 1
    i = tup[ind][0]



#replace Rare words
flag = len(probably) > 0
ind = 0
i = 0
ttt = prepared_cipher_text
pt_stat = prepared_cipher_text
c = 0
while flag:
    w = list(probably[i][0])
    r = list(probably[i][1][c])
    print(w, r)
    for j in range(len(w)):
        ttt = ttt.replace(w[j], r[j].upper())
        try:
            USED.remove(r[j])
        except:
            continue

    print(ttt)
    if (c + 1 < len(probably[i][1])):
        flag_1 = int(input(f"Взять следующее слово для подстановки? это будет слово: {probably[i][1][c + 1]}: "))
    else:
        flag_1 = False

    if flag_1:
        c += 1
        ttt = pt_stat

    else:
        flag = int(input(f"Переход к новому типу:"))
        i += 1
        pt_stat = ttt
#----

def round(ttt):
    words = replace_dots(ttt)

    words = words.split(' ')
    words = sorted(words, key=len, reverse=True)
    rrr = []
    for elem in words:
        if elem.lower() != find_regular2(elem, USED).rstrip('$'):
            o = find_all_mask(list_of_words, find_regular2(elem, USED))
            rrr.append((len(o), -len(elem), o, elem))

    rrr = sorted(rrr)

    fl = True
    i = 0
    while fl:
        if rrr[i][0] == 0:
            1 == 1
        elif rrr[i][0] > 1:
            fl = False
        else:
            w = list(rrr[i][3])
            r = list(rrr[i][2][0])

            for j in range(len(w)):
                ttt = ttt.replace(w[j], r[j].upper())
                try:
                    USED.remove(r[j])
                except:
                    continue
        i += 1
        if (i >= len(rrr)):
            fl = False
        print(i)

    return ttt


#-----

t1 = round(ttt)
t2 = round(t1)
t3 = round(t2)
print(ttt)
print(t1)
print(t2)
print(t3)
t4 = round(t3)
print(t4)
print(USED)