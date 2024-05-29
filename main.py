from Preparation_funct import get_type_vect, find_all_mask, get_regular
import pandas as pd
from string import punctuation
from nltk import tokenize


#MAIN FUNCTION. It's in the main.py file due to usage of global variables
def round(W_and_T, USED, df):
    global score_global, res_global, TABLE
    STOP = 150 #boundary of checking possible substitutions
    score = 0
    subst_list = [] #list of: (number of possible substitutions, partially decrypted word, pattern of the word

    for word, type in W_and_T:
        temp = find_all_mask(DATA[type], get_regular(word, USED)) #find possible variants by mask
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

    print(subst_list, score) #print current state

    if (ind < len(subst_list)) and (subst_list[ind][0] < STOP): #
        current_word = subst_list[ind][1]
        sss = subst_list.copy()
        q = find_all_mask(DATA[sss[ind][2]], get_regular(current_word, USED))
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
                    TABLE[w_l[j]] = r_l[j].upper()
            new_words = new_words.split()
            temp = []

            for i in range(len(subst_list)):
                temp2 = find_all_mask(DATA[sss[ind][2]], get_regular(new_words[i], list(set(USED) - set(r_l))))
                temp.append((len(temp2), new_words[i], subst_list[i][2]))
            subst_list = temp
            temp = []
            for i in range(len(subst_list)):
                temp.append((subst_list[i][1], subst_list[i][2]))
            round(temp, set(USED) - set(r_l), df)


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








#init and preparation
plaint_text = "Иуда раздражался и визгливо кричал, что он все это сам  видел и сам слышал, но упрямый Фома продолжал допрашивать неотвязчиво и спокойно, пока Иуда не сознавался, что солгал, или не сочинял новой правдоподобной лжи, над которою тот надолго задумывался. И, найдя ошибку, немедленно приходил и равнодушно уличал лжеца."
cipher_text = "КХЁВ ТВЙЁТВИВНУБ К ДКЙЕНКДР МТКЩВН, ЩФР РП ДУЖ ЯФР УВО  ДКЁЖН К УВО УНЭЪВН, ПР ХСТБОЭЛ ЦРОВ СТРЁРНИВН ЁРСТВЪКДВФЮ ПЖРФДБЙЩКДР К УСРМРЛПР, СРМВ КХЁВ ПЖ УРЙПВДВНУБ, ЩФР УРНЕВН, КНК ПЖ УРЩКПБН ПРДРЛ СТВДЁРСРЁРГПРЛ НИК, ПВЁ МРФРТРА ФРФ ПВЁРНЕР ЙВЁХОЭДВНУБ. К, ПВЛЁБ РЪКГМХ, ПЖОЖЁНЖППР СТКЧРЁКН К ТВДПРЁХЪПР ХНКЩВН НИЖШВ."
ct = cipher_text.lower()

#table of letters
TABLE = dict()
for i in range(32):
    TABLE[chr(ord('а') + i)] = ''
TABLE['ё'] = ''

#find_words and delete punctuation
tw = tokenize.TweetTokenizer()
words = tw.tokenize(ct)
words = list(filter(lambda x: x not in punctuation, words))
words = sorted(words, key=len, reverse=True)

#Divide words into two groups: len >= L_lim and len < L_lim
long_words = words[:3] #We are sure that the cipher text has got at least 3 words
short_words = []
res_global = []
score_global = 0
L_lim = len(long_words[-1]) #min len
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
S = [] #a list of pairs (word, type of word)
for i in range(len(types_of_long_words)):
    S.append((long_words[i], types_of_long_words[i]))

#open file and create a df with all words
df = pd.read_csv("Dictionaries/New_types.txt", sep=",", header=None)
df.columns = ["lemma", "type", "ipm"]
df = df.sort_values(by='ipm', ascending=False)

DATA = dict()

#Add {pattern: all possible words} for each pattern in long_words
for elem in types_of_long_words:
    temp = df.loc[df["type"] == elem]
    if elem not in DATA:
        DATA[elem] = temp['lemma'].tolist()



#------------------------ work of program
NOT_USED_letters =  [chr(ord('а') + i) for i in range(32)]
NOT_USED_letters.append('ё')
round(S, NOT_USED_letters, df)

#print substitutions
#for elem in res_global:
    #print(elem)


res = ct
key = ''

for let in TABLE:
    if TABLE[let] != '':
        res = res.replace(let, TABLE[let])
        key += TABLE[let]
    else:
        key += '_'

print(f"The key (for абвгдежзийклмнопрстуфхцчшщъыьэюяё) is: {key}")
print(f"\nCiphertext: {ct}\n\nPlaintext: {res}")
