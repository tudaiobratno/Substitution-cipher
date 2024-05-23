from Preparation_funct import get_type_vect
import numpy as np
import pandas as pd
from string import punctuation
from nltk import tokenize

#init and preparation
plaint_text = "Иуда раздражался и визгливо кричал, что он все это сам видел и сам слышал, но упрямый Фома продолжал допрашивать неотвязчиво и спокойно, пока Иуда не сознавался, что солгал, или не сочинял новой правдоподобной лжи, над которою тот надолго задумывался. И, найдя ошибку, немедленно приходил и равнодушно уличал лжеца."

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

df = pd.read_csv("New_types.txt", sep=",", header=None)
df.columns = ["lemma", "type", "ipm"]

long_df = pd.DataFrame({"word": long_words, 'type': [types_of_long_words]})
for elem in types_of_long_words:
    temp = df.loc[df["type"] == elem]
    print(temp.shape[0])


