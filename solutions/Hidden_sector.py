import pandas as pd
import itertools
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

def get_hidden_sector(input_list):

    pares = list(itertools.combinations_with_replacement(input_list, 2))
    Ss = set(
        ([abs(sum(p)) for p in pares])
    )  # Valores que se pueden obtener con los pares: S

    pares_finales = []
    for s in Ss:
        # Seleccionan los pares que satisfacen a S
        pares_dummy = [
            cumple for cumple in pares if abs(sum(cumple)) == s
        ]
        # Aplana la lista pares_dummy y deja los elementos no repetidos
        flatten_dummy = set(
            [y for x in pares_dummy for y in x]
        )
        # Genera la diferencia entre la lista original de soluciones con
        # la lista aplanada
        differ = set(input_list).difference(
            flatten_dummy
        )

        # Si no hay diferencia con la lista original, entonces se guarda
        if not differ:
            dup = {
                f"{x}": input_list.count(x)
                for x in input_list
                if input_list.count(x) > 1
            }
            if len(dup) // 2 or len(dup) == 0:
                pares_finales += [{"S": s, "ψ": pares_dummy}]

    if len(pares_finales) == 0:
        pares_finales += []

    return pares_finales


assert get_hidden_sector([2, -3, 4, -5, 11])[0].get("S") == 6
assert get_hidden_sector([2, 2, -3, 4, 4, -5, 11])[0].get("S") == 6
assert get_hidden_sector([2, 2, -3, 4, -5, 11]) == []


df["hidden"] = df["solution"].apply(get_hidden_sector)

print("*" * 20)
#print(df.iloc[0].to_dict())
df2=df[df['hidden'].apply(len)>0].reset_index(drop=True)
print(df2)
print(df2.shape)
print(get_hidden_sector([2, 2, -3, 4, 4, -5, 11]))
df2.to_json('lina.json',orient='records')