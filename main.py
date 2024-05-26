from Preparation_funct import get_type_vect, get_dataframe, get_regular, get_type
import pandas as pd
from string import punctuation
from nltk import tokenize

#init and preparation
plaint_text = "Иуда раздражался и визгливо кричал, что он все это сам  видел и сам слышал, но упрямый Фома продолжал допрашивать неотвязчиво и спокойно, пока Иуда не сознавался, что солгал, или не сочинял новой правдоподобной лжи, над которою тот надолго задумывался. И, найдя ошибку, немедленно приходил и равнодушно уличал лжеца."

cipher_text = "МЧЖВ УВЙЖУВИВРХБ М ДМЙЕРМДФ ПУМЫВР, ЫЦФ ФТ ДХЗ ЯЦФ ХВС ДМЖЗР М ХВС ХРЭЬВР, ТФ ЧОУБСЭН ШФСВ ОУФЖФРИВР ЖФОУВЬМДВЦЮ ТЗФЦДБЙЫМДФ М ХОФПФНТФ, ОФПВ МЧЖВ ТЗ ХФЙТВДВРХБ, ЫЦФ ХФРЕВР, МРМ ТЗ ХФЫМТБР ТФДФН ОУВДЖФОФЖФГТФН РИМ, ТВЖ ПФЦФУФА ЦФЦ ТВЖФРЕФ ЙВЖЧСЭДВРХБ. М, ТВНЖБ ФЬМГПЧ, ТЗСЗЖРЗТТФ ОУМЩФЖМР М УВДТФЖЧЬТФ ЧРМЫВР РИЗЪВ."
ct = cipher_text.lower()

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

def list_f(S, L, df):
    global score_global, res_global
    subst_list = []
    Len = len(S)
    score = 0
    words = []
    types = []
    #ищу датафрейм для каждого слова
    for word, type in S:
        words.append(word)
        types.append(type)
        temp = get_dataframe(word, df[df["type"] == type], L, 'lemma')
        subst_list.append([temp.shape[0], word, type])

    subst_list = sorted(subst_list)
    ind = 0
    print(subst_list)
    #пропускаю 0 и 1 - уже известные или совсем неизвестные слова
    while (ind < Len) and (subst_list[ind][0] == 0):
        ind += 1
    while (ind < Len) and (subst_list[ind][0] == 1):
        if subst_list[ind][0] != subst_list[ind][0].upper():
            q = get_dataframe(w, df[df["type"] == t], L, 'lemma')['lemma'][0]
            w_l, r_l = list(w), list(new_subst)
            for j in range(len(w_l)):
                words_str = words_str.replace(w[j], r_l[j].upper())  # замена букв
        ind += 1
        score += 1

    #проверка, где остановился индекс
    while (ind < Len):
        #где остановились
        w, t = subst_list[ind][1], subst_list[ind][2]

        #делаем подбор для каждого возможного слова
        for new_subst in get_dataframe(w, df[df["type"] == t], L, 'lemma')['lemma']:
            #копируем данные
            copy_of_words = words.copy()
            copy_of_types = types.copy()
            #строка из слов для замены
            words_str = ' '.join(copy_of_words)
            #множество букв в новом слове. Если там есть та, которую мы уже использовали, отменяем подстановку
            sub_letters = set(list(new_subst))
            if len(sub_letters - set(L)) == 0:
                w_l, r_l = list(w), list(new_subst)
                for j in range(len(w_l)):
                    words_str = words_str.replace(w[j], r_l[j].upper()) #замена букв
                copy_of_words = words_str.split()
                new_S = []
                for i in range(len(copy_of_words)):
                    new_S.append((copy_of_words[i], copy_of_types[i])) #составили новый список с учетом замены
                print("before", new_S, list(set(L) - sub_letters))
                list_f(new_S, list(set(L) - sub_letters), df) #идем в рекурсию
        ind += 1



    else:
       # print("CHECK:" , subst_list)
        if score > score_global:
            score_global = score
            res = []
            for i in subst_list:
                res.append(i[1])
            res_global = [res]
        if score == score_global:
            res = []
            for i in subst_list:
                res.append(i[1])
            res_global.append(res)


#-------------------------

k = "АДСОБЩЛСРРЮМ".lower().split()
s = []
for elem in k:
    s.append((elem, get_type(elem)))
#s = [("ШкОлА", '0.1.2.3.4', 1), ("ШкОЛА", '0.1.2.3.4', 2), ("ШКОЛА", '0.1.2.3.4', 3)]
L =  [chr(ord('а') + i) for i in range(32)]
list_f(s, L, df)
print(res_global)

