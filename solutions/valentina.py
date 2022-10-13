import numpy as np
import pandas as pd
import itertools
import collections
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
    com_index = np.array(list(itertools.combinations_with_replacement(range(len(l)),2)))

    suma = set([abs(sum(i)) for i in com])

    final = []

    for s in suma:

        cond = [i for i in com if abs(sum(i))==s]
        aux = [item for item, count in collections.Counter(cond).items() if count > 1]

        com_new = np.array(com)
        aux_new = np.array(aux)

        mask = [(i == com_new).all(axis=1) for i in aux_new]

        def_index = [com_index[mask[i]].tolist() for i in range(len(mask))]

        com_index_new = [list(itertools.combinations(i,2)) for i in def_index]
        aplanar_e  = [[[l for k in j for l in k] for j in i] for i in com_index_new]

        TF = np.array([np.array([len(j) != len(set(j)) for j in i]).all() for i in aplanar_e]).any()

        if TF.any():
            continue

        else:
            aplanar = set([item for sublist in cond for item in sublist])
            resta = set(l).difference(aplanar)

            if not resta:
                final.append({'S':s, 'ψ':set(cond)})

    return final

assert get_hidden_sector([1,2,-3,4,5])[0].get('S')==6
assert get_hidden_sector([1,2,-3,-3,4,5])[0].get('S')==6
assert get_hidden_sector([1,1,2,-3,-3,4,5,5])[0].get('S')==6
#aψ1ψ1+bψ1ψ2+cψ1,ψ3 → https://www.wolframalpha.com/input?i=Rank%20{{a,b,c},{b,0,0},{c,0,0}}
assert get_hidden_sector([1,2,-3,4,5,9,9])==[]
get_hidden_sector([1,1,2,-3,4,5])
#aψ1ψ2+bψ1ψ3 → https://www.wolframalpha.com/input?i=rank+{{0,a,b},{a,0,0},{b,0,0}}
assert get_hidden_sector([1,1,2,-3,4,5])==[]
assert get_hidden_sector([1,1,2,-3,-3,4,5])==[]
assert get_hidden_sector([1,2,-3,4,5,8])==[]
assert get_hidden_sector([1,2,-3,4,5,8,8])==[]
assert get_hidden_sector([])==[]
assert get_hidden_sector([1, 1, 1, 1, 1, -2, -2, -2, -2, 3])==[]
assert get_hidden_sector([1, 2, 2, 2, -3, -5, -6, 7])[0].get('S')==4
assert get_hidden_sector( [1, 2, 2, 4, -5, -5, -7, 8] )[0].get('S')==3
# Ana test
assert get_hidden_sector([2, -3, -4, 5, -6, 7, 7, -8])[0].get('S')==1
assert get_hidden_sector([3, 5, -8, 9, -10, -14, 15])==[] # Dirac triplet [-10,5,15] (s=5)
assert get_hidden_sector([3, 5, -8, 9, -10, -14, 15, 20,-30, 35])==[]
  
# df['hidden']=df['solution'].apply(get_hidden_sector)

# print('*'*20)
# print(df.iloc[0].to_dict())
