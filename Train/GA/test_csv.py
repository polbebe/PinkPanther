import pandas as pd

df = pd.read_csv('GA_Test_0.0.0.csv')

a = df['Best Values'].to_numpy()

print(a[0])