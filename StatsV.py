# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 01:33:41 2020

@author: HRV
"""

from statistics import mean
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np

homeDir = "C:/Users/HRV/Desktop/Post-U/Trabajo/Prueba/Data/Eventos/imgs/"
#Estaciones seleccionadas para graficas
dfsN = pd.read_csv("C:/Users/HRV/Desktop/Post-U/Trabajo/Prueba/Data/Eventos/Resumen_estaciones_P.csv")
#Data de estaciones completa
dfs = pd.read_csv("C:/Users/HRV/Desktop/Post-U/Trabajo/Prueba/Data/Eventos/bugFree_estaciones.csv")
#Copia
df2 = dfs.copy()
#Filtrado por estación 
Ests = df2['Est']

LB = ['Prof', 'mag','Dist (km) ']

TopEsts = dfsN['Est']
TopEsts = TopEsts[0:20]

for name in TopEsts:
    #Filtro el nombre
    df3 = df2[df2['Est'].isin([name])]
    var = df3[LB[2]]
    
    fig, ax = plt.subplots(figsize=(8,8))
    plt.hist(var, density=True)
    plt.title(name+', media: '+str(round(mean(var),3)))
    plt.ylabel('Probabilidad') 
    plt.xlabel('Distancia a evento (kms)') 
    plt.show() 
    