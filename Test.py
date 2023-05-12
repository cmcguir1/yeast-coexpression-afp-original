import pandas as pd
import numpy as np

data = pd.read_csv('./PTC-Data.csv').to_numpy()
print(data)
homoDom = 0
homoRec = 0 
hetero = 0

taste = 0
noTaste = 0
for row in data:
    print(row[2])
    if(row[1] == 'TT'):
        homoDom += 1
    elif(row[1] == 'Tt'):
        hetero += 1
    elif(row[1] == 'tt'):
        homoRec +=1
    if(row[2] == 'non-taster'):
        noTaste += 1
    elif(row[2] == 'taster'):
        taste += 1


print(f'HomoDom: {homoDom}')
print(f'HomoRec: {homoRec}')
print(f'Hetero: {hetero}')
print(f'Taste: {taste}')
print(f'No Taste: {noTaste}')

