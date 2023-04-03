import pandas as pd

GoTerms = pd.read_csv('./src/PairwiseYeastNetwork/GOTermIndexDictionary.csv').values.tolist()
cols = ['Gene A','Gene B']
for term in GoTerms:
    cols.append(term[0])
print(cols)