import pandas as pd
import os
import numpy as np
import itertools
import collections

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
    
    l_new = np.unique(l,return_counts = True)
    com = list(itertools.combinations_with_replacement(l,2))
    suma = set([abs(sum(i)) for i in com])
    
    final = []

#------------------------------------------------------------------------------------------------------------------

    for s in suma:
        
        cond = [i for i in com if abs(sum(i))==s]

        if len(l)%2 == 0:
            m = int(len(l)/2)
            a = np.array(list(itertools.combinations(cond,m)))
            com_cond = [np.sort(i.flatten()) for i in a]
            
            if len(com_cond) != 0:
                result = np.unique(a[(com_cond == np.sort(np.array(l))).all(axis =1)], axis = 0).tolist()
                if not result:
                    final.append([])
                else:
                    final.append({'S': s, 'ψ':[tuple(x) for x in result[0]]})
            else:
                continue
        
        else:
            m = int(len(l)/2) + 1
            a = np.array(list(itertools.combinations(cond,m)))
            aux = np.unique(np.array(cond)[np.array([len(np.unique(i)) == 1 for i in cond])])
            sself = [item for item, count in collections.Counter(l).items() if count == 1 and item in aux]
   
            com_cond = [np.unique(i,return_counts=True) for i in a]

            i = 0
            index = []

            for l2,l2_cuentas in com_cond:
                if len(l2_cuentas) == len(l_new[1]):
                    if (np.isin(l_new[0][~(l_new[1] == l2_cuentas)],sself)).all():
                        if (l2_cuentas[~(l_new[1] == l2_cuentas)] == l_new[1][~(l_new[1] == l2_cuentas)]+1).all() and np.array([len(np.unique(j))==1 for j in a[i]]).any():
                            index.append(i)
                        
                i+=1

            if not index:
                final.append([]) 
            else: 
                result = np.unique(a[np.array(index)],axis=0).tolist()
                final.append({'S': s, 'ψ':[tuple(x) for x in result[0]]})
                
    return [x for x in final if x]

#------------------------------------------------------------------------------------------------------------------
# TESTS
#------------------------------------------------------------------------------------------------------------------

assert get_hidden_sector([1,2,-3,4,5])[0].get('S')==6
assert get_hidden_sector([1,2,-3,-3,4,5])[0].get('S')==6
assert get_hidden_sector([1,1,2,-3,-3,4,5,5])[0].get('S')==6

# # aψ1ψ1+bψ1ψ2+cψ1,ψ3 → https://www.wolframalpha.com/input?i=Rank%20{{a,b,c},{b,0,0},{c,0,0}}

assert get_hidden_sector([1,2,-3,4,5,9,9])==[]

# # aψ1ψ2+bψ1ψ3 → https://www.wolframalpha.com/input?i=rank+{{0,a,b},{a,0,0},{b,0,0}}

assert get_hidden_sector([1,1,2,-3,4,5])==[]
assert get_hidden_sector([1,1,2,-3,-3,4,5])==[]
assert get_hidden_sector([1,2,-3,4,5,8])==[]
assert get_hidden_sector([1,2,-3,4,5,8,8])==[]
assert get_hidden_sector([])==[]
assert get_hidden_sector([1, 1, 1, 1, 1, -2, -2, -2, -2, 3])==[]
assert get_hidden_sector([1, 2, 2, 2, -3, -5, -6, 7])[0].get('S')==4
assert get_hidden_sector( [1, 2, 2, 4, -5, -5, -7, 8] )[0].get('S')==3

# # Ana tests

assert get_hidden_sector([2, -3, -4, 5, -6, 7, 7, -8])[0].get('S')==1
assert get_hidden_sector([3, 5, -8, 9, -10, -14, 15])==[] 

assert get_hidden_sector([3, 5, -8, 9, -10, -14, 15, 20,-30, 35])==[]   

# Tests indefinidos
  
print(f'\nPara l = [1,1,2,-3,4,5], get_hidden_sector = {get_hidden_sector([1,1,2,-3,4,5])}\n')
print(f'Para l = [-10,5,15], get_hidden_sector = {get_hidden_sector([-10,5,15])}\n')

# df['hidden']=df['solution'].apply(get_hidden_sector)

# print('*'*20)
# print(df.iloc[0].to_dict())
