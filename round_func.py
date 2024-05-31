from Preparation_funct import get_type_vect, find_all_mask, get_regular


res_global = []
table_global = []
score_global = 0

def round_f(W_and_T, used, df, table, DATA):
    global score_global, res_global, table_global
    STOP = 150 #boundary of checking possible substitutions
    score = 0
    subst_list = [] #list of: (number of possible substitutions, partially decrypted word, pattern of the word

    for word, type in W_and_T:
        temp = find_all_mask(DATA[type], get_regular(word, used)) #find possible variants by mask
        subst_list.append((len(temp), word, type))

    subst_list = sorted(subst_list)
    ind = 0 #start walking through list

    #skip 0 - words which we can't decrypt by dictionary. We will not count them for score
    while (ind < len(subst_list)) and (subst_list[ind][0] == 0):
        ind += 1

    FLAG = subst_list[ind][0] == 1

    while (ind < len(subst_list)) and FLAG:  #count decrypted words
        current_word = subst_list[ind][1]
        if current_word.isupper():
            score += 1
            ind += 1
        else:
            FLAG = False

    if (len(subst_list) - ind + score) < score_global: #There is no sense in continuing if we see that after decrypting other words the score will be lower than the maximum we have already found
        return 0

    ####    print(subst_list, score) #print current state
    table_before = table.copy()
    if (ind < len(subst_list)) and (subst_list[ind][0] < STOP): #
        current_word = subst_list[ind][1]
        sss = subst_list.copy()
        q = find_all_mask(DATA[sss[ind][2]], get_regular(current_word, used))
        for subst_word in q:

            subst_list = sss
            temp = []
            for j in range(len(subst_list)):
                temp.append(subst_list[j][1])
            new_words = ' '.join(temp)

            w_l, r_l = list(current_word), list(subst_word)
            for j in range(len(w_l)):
                if (w_l[j]) != (w_l[j].upper()):
                    new_words = new_words.replace(w_l[j], r_l[j].upper())
                    table[w_l[j]] = r_l[j].upper()
            new_words = new_words.split()
            temp = []

            for i in range(len(subst_list)):
                temp2 = find_all_mask(DATA[sss[ind][2]], get_regular(new_words[i], list(set(used) - set(r_l))))
                temp.append((len(temp2), new_words[i], subst_list[i][2]))
            subst_list = temp
            temp = []
            for i in range(len(subst_list)):
                temp.append((subst_list[i][1], subst_list[i][2]))
            round_f(temp, set(used) - set(r_l), df, table.copy(), DATA)


    if score > score_global:
        score_global = score
        res = []
        for i in subst_list:
            res.append(i[1])
        res_global = [res]
        table_global = [table]

    elif score == score_global:
        res = []
        for i in subst_list:
            res.append(i[1])
        if res not in res_global:
            res_global.append(res)
        table_global.append(table)

    return table_global