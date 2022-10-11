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
df=df[:10000]

def get_hidden_sector(l):

    com = list(itertools.combinations_with_replacement(l, 2))
    suma = set([abs(sum(i)) for i in com])

    final = []

    for s in suma:
        cond = [i for i in com if abs(sum(i)) == s]
        aplanar = [item for sublist in cond for item in sublist]
        resta = set(l).difference(set(aplanar))

        if not resta:
            l_ = l
            cond_ = cond
            N = len(l)

            combs = []

            equal = [par for par in cond_ if par[0] == par[1]]

            for par in equal:
                ind = []
                for val in par:
                    try:
                        ind.append(l_.index(val))
                    except:
                        pass
                for ind_ in ind:
                    l_[ind_] = 0

                if len(set(ind)) == 1:
                    N = N - 1
                elif len(set(ind)) != 1:
                    N = N - len(set(ind))

                combs.append(par)

            ind_eq = [cond.index(eq) for eq in equal]
            for ind in ind_eq:
                cond_.pop(ind)

            for par in cond_:
                try:
                    for val in par:
                        l_[l_.index(val)] = 0
                    N = N - 2
                    combs.append(par)
                except:
                    pass
                    # print("Discharge pair", par)

            if N == 0:
                final.append({"S": s, "ψ": combs})

            del l_, cond_

    return final


df["hidden"] = df["solution"].apply(get_hidden_sector)

print("*" * 20)
#print(df.iloc[0].to_dict())
df2=df[df['hidden'].apply(len)>0].reset_index(drop=True)
print(df2)
print(df2.shape)
