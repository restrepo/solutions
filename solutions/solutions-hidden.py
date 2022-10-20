#!/usr/bin/env python3

# librerias
import numpy as np
import pandas as pd
from itertools import permutations

# definición de función


def get_hidden_sector(qin):
    """
    Obtiene la masa y los pares que generan masa a las
    soluciones quirales del grupo de simetria U1
    INPUT: qin - array o lista
    OUTPUT: list - dicts {'S': int, 'Psi': array}
    """
    q = np.array(qin)
    M = np.abs(np.add.outer(q, q))
    sumas = np.unique(M)
    s_ = []
    for suma in sumas:
        ub_s = np.asarray(M == suma).nonzero()

        # garantiza al menos una pareja con ese entero
        if np.unique(ub_s[0]).shape[0] == M.shape[0]:
            s_.append(suma)

    all_hidden = []
    # recorre todas las sumas posibles
    if len(s_) != 0:
        # armar pares
        for s in s_:
            # inicia los pares
            hidden = []
            tmp_M = np.asarray(np.triu(M) == s).nonzero()
            pairs = np.array(
                [[q[tmp_M[0][i]], q[tmp_M[1][i]]] for i in range(0, tmp_M[0].shape[0])]
            )

            # agregar condiciones sobre los pares
            if pairs.flatten().shape[0] == q.shape[0] and np.sort(pairs.flatten()) == np.sort(q):
                hidden = {"S": s, "ψ": pairs}
                continue
            else:
                # casos no obvios
                # n_pairs = round(q.shape[0] / 2, 0)
                N = q.shape[0]
                q_ = q.copy()

                eq_pairs = [p for p in pairs if p[0] == p[1]]
                dif_pairs_ = [p for p in pairs if p[0] != p[1]]
                all_dif = permutations(np.unique(dif_pairs_, axis=0))

                for dif_pairs in all_dif:

                    true_pairs = []

                    for pair in dif_pairs:
                        # para pares que tomen los elementos
                        if (
                            np.where(q_ == pair[0])[0].shape[0] != 0
                            and np.where(q_ == pair[1])[0].shape[0] != 0
                        ):
                            q_[np.where(q_ == pair[0])[0][0]] = 0
                            q_[np.where(q_ == pair[1])[0][0]] = 0
                            true_pairs.append(pair)
                            N -= 2

                    for pair in eq_pairs:
                        # si está una vez
                        if np.where(q_ == pair[0])[0].shape[0] == 1:
                            q_[np.where(q_ == pair[0])[0][0]] = 0
                            true_pairs.append(pair)
                            N -= 1
                        elif np.where(q_ == pair[0])[0].shape[0] > 1:
                            q_[np.where(q_ == pair[0])[0][0]] = 0
                            q_[np.where(q_ == pair[1])[0][0]] = 0
                            true_pairs.append(pair)
                            N -= 2

                    if N == 0:
                        hidden = {"S": s, "ψ": true_pairs}
                        break
            if hidden != []:
                all_hidden.append(hidden)
    else:
        hidden = []

    return all_hidden


# pruebas del hidden sector
assert get_hidden_sector([1, 2, -3, 4, 5])[0].get("S") == 6
assert get_hidden_sector([1, 2, -3, -3, 4, 5])[0].get("S") == 6
assert get_hidden_sector([1, 1, 2, -3, -3, 4, 5, 5])[0].get("S") == 6
assert get_hidden_sector([1, 2, -3, 4, 5, 9, 9]) == []
get_hidden_sector([1, 1, 2, -3, 4, 5])
assert get_hidden_sector([1, 1, 2, -3, 4, 5]) == []
assert get_hidden_sector([1, 1, 2, -3, -3, 4, 5]) == []
assert get_hidden_sector([1, 2, -3, 4, 5, 8]) == []
assert get_hidden_sector([1, 2, -3, 4, 5, 8, 8]) == []
assert get_hidden_sector([]) == []
assert get_hidden_sector([1, 1, 1, 1, 1, -2, -2, -2, -2, 3]) == []
assert get_hidden_sector([1, 2, 2, 2, -3, -5, -6, 7])[0].get("S") == 4
assert get_hidden_sector([1, 2, 2, 4, -5, -5, -7, 8])[0].get("S") == 3
# Ana test
assert get_hidden_sector([2, -3, -4, 5, -6, 7, 7, -8])[0].get("S") == 1
assert (
    get_hidden_sector([3, 5, -8, 9, -10, -14, 15]) == []
)  # Dirac triplet [-10,5,15] (s=5)
assert get_hidden_sector([3, 5, -8, 9, -10, -14, 15, 20, -30, 35]) == []
# test nicole
assert get_hidden_sector([1, -4, -5, 7, -10, 13, 14, -16])[0].get("S") == 9
assert get_hidden_sector([1, -3, -9, 10, -12, 14, 20, -21])[0].get("S") == 11
