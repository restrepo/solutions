import pandas as pd
import os
if not os.path.exists('solutions.json'):
    print('remote loading')
    df=pd.read_json('https://zenodo.org/record/5526707/files/solutions.json?download=1')
    df.to_json('solutions.json',orient='records')
else:
    print('local loading')
    df=pd.read_json('solutions.json')

print(df.shape)
print(df.columns)
def get_hidden_sector(l):
  return []


df['hidden']=df['solution'].apply(get_hidden_sector)

print('*'*20)
print(df.iloc[0].to_dict())
