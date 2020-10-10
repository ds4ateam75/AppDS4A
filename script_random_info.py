# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 02:59:45 2020

@author: juanp
"""
import pandas as pd
import numpy as np
import datetime as dt
docs = ['1001',
        '1002',
        '1003'
        ]

dfs = []
for doc in docs:
    dfs.append(pd.read_csv(r'C:\Users\juanp\OneDrive\Escritorio\AppDS4A\rutas_ejemplo\{}.csv'.format(doc)))

df = pd.concat(dfs,axis = 0)
del(dfs)
del(doc)
df.reset_index(inplace = True,drop = True)

df_sim = pd.DataFrame()

for indice in range(200000):
    df_sim.at[indice,'hora'] = int(np.random.uniform(low = 0 , high = 23))
    df_sim.at[indice,'fecha'] = dt.date(2020, 10, int(np.random.uniform(low = 1 , high = 11)))
    x = int(np.random.uniform(low = 0 , high = 2719))
    df_sim.at[indice,'ruta'] = df.at[x,'ruta']
    df_sim.at[indice,'longitud'] = df.at[x,'longitud']
    df_sim.at[indice,'latitud'] = df.at[x,'latitud']


for indice in range(200000):
    df_sim.at[indice,'carga'] = int(np.random.uniform(low = 0 , high = 60))


df_sim.to_csv(r'C:\Users\juanp\OneDrive\Escritorio\AppDS4A\rutas_ejemplo\ejemplo_info.csv',index = False)


if 4:
    print(True)