import pandas as pd

df = pd.read_csv('Errors.csv')

print(df.mean(axis=0))
