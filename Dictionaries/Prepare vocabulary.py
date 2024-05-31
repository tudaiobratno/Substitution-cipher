import pandas as pd
#import pymorphy2
#It's possible to increase dictionary of words and types by adding new forms of particular words. It's easy to do with pymorphy lib

def get_type(s):
    temp = list(s)
    used = dict()
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


file = open("New_types.txt", 'w')
df = pd.read_csv("russian.utf-8", header=None)
df.columns = ["Lemma"]
df_freq = pd.read_csv("Type_dict.txt", sep=' ', header=None)
df_freq.columns = ["word", "_", "ipm"]
u = df["Lemma"].unique()
#morph = pymorphy2.MorphAnalyzer()
for elem in u:

    #extra for pymorhy. Works incorrectly
    '''word = elem
    parsed_word = morph.parse(word)[0]
    word_forms = parsed_word.lexeme
    all_forms = []
    for form in word_forms:
        all_forms.append(form.word)
    all_forms = list(set(all_forms))'''

    result = df_freq.loc[df_freq['word'] == elem]
    k = result.shape
    if k[0] != 0:
        f = result.iloc[0, 2]
        file.write(elem + ',' + get_type(elem) + ',' + str(f) + '\n') #frequency from the known data
    else:
        file.write(elem + ',' + get_type(elem) + ',' + str(0.01) + '\n')


print("finished")
file.close()