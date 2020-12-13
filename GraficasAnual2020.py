# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 04:31:56 2020

@author: Steven RV

Generacion de gráficas para informe 2020
"""

import pandas as pd
from datetime import date
#import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#Funcion para generar el número de día del año
def DayNumer2020(a):
    d0 = date(int(a[0:4]), int(a[5:7]), int(a[8:10]))
    d1 = date(2018,12,31)
    delta = d0 - d1
    return(delta.days)

#Funcion para generar fecha manejada en GT
def GtFormat(a):
    dia = a[8:10]+'-'+a[5:7]+'-'+a[0:4]
    return dia

#Lectura de .csv con la data    
dfs = pd.read_csv('Data/Data2019-20.csv')

#Filtramos folders y magnitud de los eventos
folders = dfs[' folder']
mag = dfs[' ml']

#Plot 1
NumDias = []
FechaDias = []
#Almaceno el numero de día de cada evento
for evento in folders:
    FechaDias.append(GtFormat(evento))
    NumDias.append(DayNumer2020(evento))
    
#Determinamos el número de semanas para la cantidad de bins
semanas = int(max(NumDias)/7)

#Figura 1
#Histograma con distribución de sismos
plt.figure(1)
plt.hist(NumDias, bins=semanas,color='#0504aa',alpha=0.7, rwidth=0.85)
#plt.grid(axis='y', color='k', linestyle='-', linewidth=1)
plt.xlabel('Número de día del año')
plt.ylabel('Cantidad de sismos')
plt.title('Actividad sismica semanal 2019-20')
plt.xlim(xmin=0,xmax = 732)
plt.axvline(x=365,linewidth=1, color='k')
plt.text(365,50,'2020',rotation=90)
sns.set_style("ticks")
sns.despine()
plt.show()

#Figura 2
#Histograma stacked por magnitud

#Listas para almacenar elemenots
mag01 = []
mag12 = []
mag23 = []
mag34 = []

#Clasificacion por rangos
for evento, mag in zip(folders,mag):
    if mag<= 2.0: 
        mag01.append(DayNumer2020(evento))
    if mag<= 3.5 and mag>2.0:
        mag12.append(DayNumer2020(evento))
    if mag<= 5.0 and mag >3.5:
        mag23.append(DayNumer2020(evento))
    if mag> 5.0:
        mag34.append(DayNumer2020(evento))
        
#Nombres para el histograma
nombres = ['<2.0','<3.5','<5.0','>5.0']

plt.figure(2)
plt.hist([mag01,mag12,mag23, mag34], bins=semanas,color=['#0504aa','r','g','m'],stacked=True,alpha=0.7, rwidth=0.85,label=nombres)
plt.legend(prop={'size': 10})
#plt.grid(axis='y', color='k', linestyle='-', linewidth=1)
plt.xlabel('Número de día del año')
plt.ylabel('Cantidad de sismos')
plt.title('Actividad sismica semanal por magnitud 2019-20')
plt.xlim(xmin=0,xmax = 732)
plt.axvline(x=365,linewidth=1, color='k')
plt.text(365,50,'2020',rotation=90)
sns.set_style("ticks")
sns.despine()
plt.show()

#Figura 3
#Histogramas por magnitud separados. 
fig, axs = plt.subplots(2, 2)
fig.suptitle('Actividad sismica semanal por magnitud 2019-20')
axs[0, 0].hist(mag01, bins=semanas,color='#0504aa',alpha=0.7, rwidth=0.85)
axs[0, 0].set_title("Magnitud <2.0 ("+str(len(mag01))+")")
axs[0, 1].hist(mag12, bins=semanas,color='r',alpha=0.7, rwidth=0.85)
axs[0, 1].set_title("Magnitud <3.5 ("+str(len(mag12))+")")
axs[1, 0].hist(mag23, bins=semanas,color='g',alpha=0.7, rwidth=0.85)
axs[1, 0].set_title("Magnitud <5.0 ("+str(len(mag23))+")")
axs[1, 1].hist(mag34, bins=semanas,color='m',alpha=0.7, rwidth=0.85)
axs[1, 1].set_title("Magnitud >5.0 ("+str(len(mag34))+")")
sns.set_style("ticks")
sns.despine()
fig.tight_layout()
