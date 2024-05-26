from Preparation_funct import get_type_vect, get_dataframe, get_regular, get_type
import pandas as pd
from string import punctuation
from nltk import tokenize

#init and preparation
plaint_text = "Иуда раздражался и визгливо кричал, что он все это сам  видел и сам слышал, но упрямый Фома продолжал допрашивать неотвязчиво и спокойно, пока Иуда не сознавался, что солгал, или не сочинял новой правдоподобной лжи, над которою тот надолго задумывался. И, найдя ошибку, немедленно приходил и равнодушно уличал лжеца."

cipher_text = "МЧЖВ УВЙЖУВИВРХБ М ДМЙЕРМДФ ПУМЫВР, ЫЦФ ФТ ДХЗ ЯЦФ ХВС ДМЖЗР М ХВС ХРЭЬВР, ТФ ЧОУБСЭН ШФСВ ОУФЖФРИВР ЖФОУВЬМДВЦЮ ТЗФЦДБЙЫМДФ М ХОФПФНТФ, ОФПВ МЧЖВ ТЗ ХФЙТВДВРХБ, ЫЦФ ХФРЕВР, МРМ ТЗ ХФЫМТБР ТФДФН ОУВДЖФОФЖФГТФН РИМ, ТВЖ ПФЦФУФА ЦФЦ ТВЖФРЕФ ЙВЖЧСЭДВРХБ. М, ТВНЖБ ФЬМГПЧ, ТЗСЗЖРЗТТФ ОУМЩФЖМР М УВДТФЖЧЬТФ ЧРМЫВР РИЗЪВ."
ct = cipher_text.lower()

TABLE = dict()
for i in range(32):
    TABLE[chr(ord('А') + i)] = ''
print(TABLE)
#find_words
tw = tokenize.TweetTokenizer()
words = tw.tokenize(ct)
words = list(filter(lambda x: x not in punctuation, words))
words = sorted(words, key=len, reverse=True)
#print(words)

#Devide words into two groups: len >= L_lim and len < L_lim

long_words = words[:3] #We are sure that the cipher text has got at least 3 words
short_words = []
res_global = []
score_global = 0

L_lim = len(long_words[-1])
ind = 3

if L_lim >= 5:
    L_lim = 5  #set a low boundary of words' length

while (ind < len(words)) and (len(words[ind]) >= L_lim):
    long_words.append(words[ind])
    ind += 1

short_words = words[ind:]


#-------- Work with long words -------------
#Create a list of types for each long word

types_of_long_words = get_type_vect(long_words)
#print(types_of_long_words)

#open file

df = pd.read_csv("Dictionaries/New_types.txt", sep=",", header=None)
df.columns = ["lemma", "type", "ipm"]
df = df.sort_values(by='ipm', ascending=False)

long_df = pd.DataFrame({"word": long_words, 'type': types_of_long_words})

for elem in types_of_long_words:
    temp = df.loc[df["type"] == elem]


#--------------check
we = "ШкОЛА"
q = get_regular(we, [chr(ord('а') + i) for i in range(32)])
t = get_dataframe(we, df[df["type"] == '0.1.2.3.4'], [chr(ord('а') + i) for i in range(32)], "lemma")
print(t)

#-----------------

def list_f(W_and_T, USED, df):
    global score_global, res_global
    score = 0
    res = []
    subst_list = []
    for word, type in W_and_T:
        temp = get_dataframe(word, df[df["type"] == type], USED, 'lemma')
        subst_list.append((temp.shape[0], word, type))

    subst_list = sorted(subst_list)
    print(subst_list)
    ind = 0
    #print(subst_list)
    # пропускаю 0 и 1 - уже известные или совсем неизвестные слова
    while (ind < len(subst_list)) and (subst_list[ind][0] == 0):
        ind += 1

    flag = subst_list[ind][0] == 1
    while (ind < len(subst_list)) and (flag):
        current_word = subst_list[ind][1]
        if current_word.isupper():
            score += 1
            ind += 1
        else:
            flag = False


    if (ind == len(subst_list)):
        if score > score_global:
            score_global = score
            res = []
            for i in subst_list:
                res.append(i[1])
            res_global = [res]
        elif score == score_global:
            res = []
            for i in subst_list:
                res.append(i[1])
            if res not in res_global:
                res_global.append(res)

    else:
        #print(subst_list)
        while (ind < len(subst_list)):
            current_word = subst_list[ind][1]
           # print(get_dataframe(current_word, df[df["type"] == subst_list[ind][2]], USED, 'lemma')['lemma'])
            sss = subst_list.copy()
            for subst_word in get_dataframe(current_word, df[df["type"] == sss[ind][2]], USED, 'lemma')['lemma'].tolist():
                #print(subst_word)
                subst_list = sss
                temp = []
                for j in range(len(subst_list)):
                    temp.append(subst_list[j][1])
                new_words = ' '.join(temp)

                w_l, r_l = list(current_word), list(subst_word)
                for j in range(len(w_l)):
                    new_words = new_words.replace(w_l[j], r_l[j].upper())
                new_words = new_words.split()
                temp = []

                for i in range(len(subst_list)):
                    temp2 = get_dataframe(new_words[i], df[df["type"] == subst_list[i][2]], set(USED) - set(r_l), 'lemma')
                    temp.append((temp2.shape[0], new_words[i], subst_list[i][2]))
                subst_list = temp
                temp = []
                for i in range(len(subst_list)):
                    temp.append((subst_list[i][1], subst_list[i][2]))
                list_f(temp, set(USED) - set(r_l), df)
            USED = list(set(USED) - set(r_l))
            ind += 1


#-------------------------

k = "Б МХЪВФЮ МВЪВ КЕТВ ЯДРНАШКРППЭЛ ЯМТВП УРНПШЖ".lower().split()
s = []
for elem in k:
    s.append((elem, get_type(elem)))
#s = [("ШкОлА", '0.1.2.3.4', 1), ("ШкОЛА", '0.1.2.3.4', 2), ("ШКОЛА", '0.1.2.3.4', 3)]
Lo =  [chr(ord('а') + i) for i in range(32)]
list_f(s, Lo, df)
for elem in res_global:
    print(elem)

