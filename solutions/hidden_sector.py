import itertools as itertools
import pandas as pd
import os

if not os.path.exists("solutions.json"):
    print("remote loading")
    df = pd.read_json(
        "https://zenodo.org/record/5526707/files/solutions.json?download=1"
    )
    df.to_json("solutions.json", orient="records")
else:
    print("local loading")
    df = pd.read_json("solutions.json")

print(df.shape)
print(df.columns)

def split_pairs(pairs):
    
    equal = [pair for pair in pairs if pair[0]==pair[1]]
    diff = [pair for pair in pairs if pair[0]!=pair[1]]

    return equal, diff

def remove_intersection(pairs):
    pairs_cp = pairs.copy()
    for pair_1 in pairs_cp:
        subpairs = pairs.copy()
        subpairs.remove(pair_1)
        inters = []
        for pair_2 in subpairs:
            if set(pair_1).intersection(pair_2):
                s = set(pair_1).intersection(pair_2)
                for x in s:
                    inters.append(x)
        inters = tuple(sorted(list(set(inters))))
        if len(inters)==2:
            try:
              ind = pairs_cp.index(inters)
              ON = True
            except:
              ON = False
            if ON:
               pairs_cp.pop(ind)
    return pairs_cp

def filter_set_pairs(pairs, l):

    N = len(l)
    l_ = l.copy()
    
    equal, diff = split_pairs(pairs)

    for pair in diff:
        ind = []
        try:
            for val in pair:
                ind.append(l_.index(val))
        except:
            pass

        if len(ind)==2:
            for ind_ in ind:
                l_[ind_] = 0
            N = N - 2
    
        #print(N, l_, pair)

    for pair in equal:
        ind = []
        for val in pair:
            try:
                ind.append(l_.index(val))
                l_[l_.index(val)] = 0
            except:
                pass
        
        if len(set(ind)) == 1:
            N = N - 1
        elif len(set(ind)) == 2:
            N = N - 2

        #print(N, l_, pair)

    if N==0 and sum(l_)==0:
        return True
    else:
        return False

def get_hidden_sector(l):
    
    combs = list(itertools.combinations_with_replacement(l,2))
    sums = set([abs(sum(i)) for i in combs])
    
    final = []

    for s in sums:
        pairs = [i for i in combs if abs(sum(i))==s]
        flatten = set([item for sublist in pairs for item in sublist])
        resta = set(l).difference(flatten)
    
        if not resta:

            FINISH = False

            for DO_INTERSECTION in [True, False]:
                
                if DO_INTERSECTION:
                    pairs_ = remove_intersection(pairs)
                else:
                    pairs_ = pairs.copy()

                ON = True

                perms = list(itertools.permutations(pairs_))[:1]

                i = 0
                while i<len(perms):

                    VALID = filter_set_pairs(list(perms[i]), l)

                    if VALID:
                        final_pairs = list(set(pairs))
                        final.append({'S':s, 'ψ':final_pairs})
                        i = len(perms)
                        FINISH = True
                        break
                    else:
                      i=i+1
                
                if FINISH:
                    break

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

df["hidden"] = df["solution"].apply(get_hidden_sector)

print("*" * 20)
#print(df.iloc[0].to_dict())
df2=df[df['hidden'].apply(len)>0].reset_index(drop=True)
print(df2)
print(df2.shape)
df2.to_json('ana.json',orient='records')
