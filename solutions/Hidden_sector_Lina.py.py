from itertools import product
from collections import Counter
import pandas as pd
import warnings
warnings.simplefilter('ignore')

def get_hidden_sector(l):
    
    def unique_everseen(iterable, key=None):    
        "List unique elements, preserving order. Remember all elements ever seen."
        # unique_everseen('AAAABBBCCDAABBB') --> A B C D
        # unique_everseen('ABBCcAD', str.lower) --> A B C D
        seen = set()
        seen_add = seen.add
        if key is None:
            for element in ifilterfalse(seen.__contains__, iterable):
                seen_add(element)
                yield element
        else:
            for element in iterable:
                k = key(element)
                if k not in seen:
                    seen_add(k)
                    yield element
                        
    duplas = list(product(l, repeat=2)) # Si [A,B,C] entonces AA AB AC, BA BB BC, CA CB CC
    n,m = set(), set()
    respuesta = []
    res = []
    for c,v in enumerate(duplas,1):
        if c <= len(l):
            n.add(abs(sum(v)))
        else:
            if c%len(l) == 0:
                m.add(abs(sum(v)))
                n = m.intersection(n)
                if c != len(duplas):
                    m = set()
                else:
                    n = n.intersection(m)
            else:
                m.add(abs(sum(v)))
    try:        
        S = list(n)[0]
        
        for i in duplas:
            if abs(sum(i)) == S:
                respuesta.append(i)
        
        gen = list(unique_everseen(respuesta, lambda x: (min(x), max(x))))
        
        for i in list(l):
            for k in list(l):
                if k != i:
                    if abs(i + k) == S:
                        try:               
                            l.remove(i)
                            l.remove(k)
                            break
                        except:
                            break
        
        for i in list(l):
            for k in list(l):
                if k == i:
                    if abs(i + k) == S:
                        try:               
                            l.remove(i)
                            l.remove(k)
                            break
                        except:
                            break
        
        if l != []:
            res = []
        else:
            res = [{'S': S, 'psi':gen}]
                
    except:
        res = []
    return res
    
assert get_hidden_sector([1,2,-3,4,5])[0].get('S')==6
assert get_hidden_sector([1,2,-3,-3,4,5])[0].get('S')==6
assert get_hidden_sector([1,1,2,-3,-3,4,5,5])[0].get('S')==6
assert get_hidden_sector([1,2,-3,4,5,9,9])==[]
assert get_hidden_sector([1,1,2,-3,4,5])==[]
assert get_hidden_sector([1,1,2,-3,-3,4,5])==[]
assert get_hidden_sector([1,2,-3,4,5,8])==[]
assert get_hidden_sector([1,2,-3,4,5,8,8])==[]
assert get_hidden_sector([])==[]
s
assert get_hidden_sector([1, 1, 1, 1, 1, -2, -2, -2, -2, 3])==[] # len(S) > 1

assert get_hidden_sector([1, 2, 2, 2, -3, -5, -6, 7])[0].get('S')==4
assert get_hidden_sector( [1, 2, 2, 4, -5, -5, -7, 8] )[0].get('S')==3
assert get_hidden_sector([2, -3, -4, 5, -6, 7, 7, -8])[0].get('S')==1
assert get_hidden_sector([3, 5, -8, 9, -10, -14, 15])==[]
assert get_hidden_sector([3, 5, -8, 9, -10, -14, 15, 20,-30, 35])==[]


df=pd.read_json('https://zenodo.org/record/5526707/files/solutions.json?download=1')
df['hidden']=df['solution'].apply(get_hidden_sector)
df1 = df[df['hidden'].map(lambda d: len(d)) > 0]
print(len(df1)) # Ya que len(S) > 1, algunas soluciones no son tenidas en cuenta puesto que este código solo tiene en cuenta len(S)=1 por ahora
df1['count'] = df1['hidden'].apply(lambda d: len(d))
print(df1['count'].sum())
