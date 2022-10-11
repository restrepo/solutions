#!/usr/bin/env python3

# librerias
import numpy as np
import pandas as pd

# funciones


def get_hidden(q1):
    """
    Obtiene la masa y los pares que generan masa a las
    soluciones quirales del grupo de simetria U1
    INPUT: q1 - array
    OUTPUT: int, array
    """

    M1 = np.abs(np.add.outer(q1, q1))

    # recorre sobre todas las sumas posibles
    for u_val in np.unique(M1):
        # encuentra la ubicación de cada entero posible
        to_v = np.asarray(M1 == u_val).nonzero()

        # garantiza que todos puedan ser emparejados con ese entero
        if np.unique(to_v[0]).shape[0] == M1.shape[0]:
            print("value = ", u_val)

            # obtiene las parejas que suman el escalar comun a todos
            nw_to_v = np.asarray(np.triu(M1) == u_val).nonzero()
            pairs = np.array(
                [
                    [q1[nw_to_v[0][i]], q1[nw_to_v[1][i]]]
                    for i in range(0, nw_to_v[0].shape[0])
                ]
            )

            # garantizando matches
            un_q = np.unique(q1)
            rep_q = [np.where(q1 == xq)[0].shape[0] for xq in un_q]

            nw_pairs = pairs.copy()
            for j in range(0, un_q.shape[0]):
                del_ind = np.where(nw_pairs == un_q[j])[0]
                if np.unique(del_ind).shape[0] != rep_q[j]:
                    nw_pairs = np.delete(nw_pairs, del_ind[rep_q[j]:], axis=0)

            print(nw_pairs)
            # agregar condicion sobre autovalores
            S = u_val
            PHI = nw_pairs.copy()

    return S, PHI
