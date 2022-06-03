import pandas as pd

data = pd.read_csv('./resources/Boston.csv').to_numpy()
total = 0
for i in range(len(data)):
    total += data[i,13]
print(f'Mean: {total / len(data)}')