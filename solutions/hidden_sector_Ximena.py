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

from posixpath import join
def get_hidden_sector(l):
    
    ps=list(itertools.combinations_with_replacement(l,2)) # Combinaciones
    Ss=set([abs(sum(p)) for p in ps]) # Suma


    #paress={} # Diccionario con los diferentes valores para ingresarlos a un dataframe
    cumplen=[] # Arreglo de las soluciones que cumplen
  
    for s in Ss:
        tmp=[p for p in ps if abs(sum(p))==s] 
        flatten=[item for sublist in tmp for item in sublist] # Aplana las listas 

        set_flatten=set(flatten)

        if not set(l).difference(set(flatten)):
            l=np.array(l)
            n=len(l)
            l_copy = l.copy()
            l_copy=np.array(l_copy)
            tmp_copy = tmp

            combinations = []

            par_igual = [pares for pares in tmp_copy if pares[0] == pares[1]]
            #ind_eq = [cond.index(eq) for eq in equal]
            
            
            for i in (tmp.index(k) for k in par_igual):
                tmp_copy.pop(i)
                #print('hi')
            
            for pares in tmp_copy:
                
                for j in pares:
                    l_copy[np.where(l == j)] = 0

                combinations+=[pares]
                n=n-2

            for p in par_igual:
                m = []
                for i in p:
                    try:
                        m+=[np.where(l == i)]
                        
                    except:
                        pass
                for j in m:
                    l_copy[j] = 0
                m=np.transpose(m)
                
                if len(set(m[0][0])) == 1:
                    n=n-1
                elif len(m[0][0]) != 1:
                    n=n-len(m[0][0])

                combinations+=[pares]

            if n==0:
              
              cumplen.append({"S": s, "sigma": combinations})

            del l_copy, tmp_copy

    return cumplen

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
  
  
df['hidden']=df['solution'].apply(get_hidden_sector)



print('*'*20)
print(df.iloc[0].to_dict())
