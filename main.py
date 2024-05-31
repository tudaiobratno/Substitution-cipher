from Preparation_funct import get_type_vect
import pandas as pd
from string import punctuation
from nltk import tokenize
from prettytable import PrettyTable
from round_func import round_f


#init and preparation
#cipher_text = "СТВДРУНВДПВБ ШЖТМРДЮ ДУСРОКПВЖФ ХУФВПРДНЖПКЖ ФВКПУФДВ ЖДЧВТКУФКК, МРФРТРЖ СТРКЙРЪНР ДР ДТЖОБ ФВЛПРЛ ДЖЩЖТК, Д ДЖНКМКЛ ЩЖФДЖТЕ. МТРОЖ ФРЕР, Д ФЖЩЖПКЖ ЕРЁВ (В ПЖ ФРНЮМР Д ДЖНКМКЛ ЩЖФДЖТЕ) ПВ НКФХТЕКК СЖТЖЁ СТКЩВЫЖПКЖО ЩКФВЖФУБ ОРНКФДВ, УРУФВДНЖППВБ КРВППРО ЙНВФРХУФРО"
cipher_text = input()
ct = cipher_text.lower()

#table of letters
table = dict()
for i in range(32):
    table[chr(ord('а') + i)] = ''
table['ё'] = ''

#find_words and delete punctuation
tw = tokenize.TweetTokenizer()
words = tw.tokenize(ct)
words = list(filter(lambda x: x not in punctuation, words))
words = sorted(words, key=len, reverse=True)

#Divide words into two groups: len >= L_lim and len < L_lim
long_words = words[:3] #We are sure that the cipher text has got at least 3 words
short_words = []

L_lim = len(long_words[-1]) #min len for finding
ind = 3
if L_lim >= 5:
    L_lim = 5 #set a low boundary of words' length. Can take values from 1 to L_lim

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
NOT_USED_letters = [chr(ord('а') + i) for i in range(32)]
NOT_USED_letters.append('ё')
possible_keys = round_f(S, NOT_USED_letters, df, table, DATA)

#print results
ind = 1
for table in possible_keys:
    res = ct
    t = PrettyTable(table.keys())
    t.add_row(table.values())
    for let in table:
        if table[let] != '':
            res = res.replace(let, table[let])
    print(f"\n\n---------------------------------\n            Key №{ind}                 \n---------------------------------")
    print(t)
    print(f"\nCiphertext: {ct}\n\nPlaintext: {res}")
    ind +=1
