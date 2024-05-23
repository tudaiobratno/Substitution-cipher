import pandas as pd
import numpy as np
from Preparation_funct import get_type

'''
#open file
file = open('Type_dict.txt', 'w')

#Обработка данных
df = pd.read_csv("rus_dict.csv")
df = df.loc[:, ~df.columns.str.startswith('Unnamed')]
df = df.drop("Часть речи", axis=1)

#Ищем похожие, выравниваем частоту
u = df["Лемма"].unique()
for elem in u:
    if elem not in dict:
        times = df['Лемма'].value_counts()[elem]
        word = df.loc[df['Лемма'] == elem]
        ipm = np.sum(word["Частота (ipm)"].values) / times
        file.write(elem + ' ' + get_type(elem) + ' ' + str(ipm) + '\n')

print("finished")
file.close()
'''

file = open("New_types.txt", 'w')
df = pd.read_csv("russian.utf-8", header=None)
df.columns = ["Lemma"]
u = df["Lemma"].unique()
for elem in u:
    file.write(elem + ',' + get_type(elem) + ',' + str(1) + '\n')

print("finished")
file.close()