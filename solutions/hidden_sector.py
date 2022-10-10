import itertools as itertools
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
    
    com = list(itertools.combinations_with_replacement(l,2))
    suma = set([abs(sum(i)) for i in com])
    
    final = []

    for s in suma:
        cond = [i for i in com if abs(sum(i))==s]
        aplanar = set([item for sublist in cond for item in sublist])
        resta = set(l).difference(aplanar)
    
        if not resta:
            final.append({'S':s, 'ψ':cond})
        
    return final

df['hidden']=df['solution'].apply(get_hidden_sector)

print('*'*20)
print(df.iloc[0].to_dict())
