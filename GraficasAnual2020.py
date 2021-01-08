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
import numpy as np

#Funcion para generar el número de día del año
def DayNumer2020(a):
    d0 = date(int(a[0:4]), int(a[5:7]), int(a[8:10]))
    #Día 0
    d1 = date(2019,12,31)
    delta = d0 - d1
    return(delta.days)

#Funcion para obtener el mes del año
def MesNumer(a):
    d0 = a[5:7]
    return(d0)

#Funcion para obtener la hora del sismoDay
def DayHour(a):
    d0 = a[11:13]
    return(int(d0))

#Funcion para generar fecha manejada en GT
def GtFormat(a):
    dia = a[8:10]+'-'+a[5:7]+'-'+a[0:4]
    return dia

#Lectura de .csv con la data    
dfs = pd.read_csv('Data/Data2020.csv')

#Filtramos folders y magnitud de los eventos
folders = dfs[' folder']
mag = dfs[' ml']

#Plot 1
NumDias = []
FechaDias = []
MesDias = []
HourD = []
#Almaceno el numero de día de cada evento
for evento in folders:
    FechaDias.append(GtFormat(evento))
    NumDias.append(DayNumer2020(evento))
    MesDias.append(MesNumer(evento))
    HourD.append(DayHour(evento))
    
#Determinamos el número de semanas para la cantidad de bins
semanas = int(max(NumDias)/7)

#Figura 1
if(True):
    #Histograma con distribución de sismos
    plt.figure(1)
    plt.hist(NumDias, bins=semanas,color='#0504aa',alpha=0.7, rwidth=0.85)
    #plt.grid(axis='y', color='k', linestyle='-', linewidth=1)
    plt.xlabel('Número de día del año')
    plt.ylabel('Cantidad de sismos')
    plt.title('Actividad sísmica semanal 2020')
    plt.xlim(xmin=0,xmax = 365)
    plt.axvline(x=365,linewidth=1, color='k')
    #plt.text(365,50,'2020',rotation=90)
    sns.set_style("ticks")
    sns.despine()
    plt.savefig('Imagenes/2020Actividad.png', bbox_inches='tight')
    plt.show()

#Figura 2
if(False):
    #Histograma stacked por magnitud
    #Listas para almacenar elementos
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
    plt.hist([mag01,mag12,mag23, mag34], bins=semanas,color=['#0504aa','r','g','m'],stacked=True,
             alpha=0.7, rwidth=0.85,label=nombres,density=False,cumulative=False)
    plt.legend(prop={'size': 10})
    #plt.grid(axis='y', color='k', linestyle='-', linewidth=1)
    plt.xlabel('Número de día del año')
    plt.ylabel('Cantidad de sismos')
    plt.title('Actividad sísmica semanal por magnitud 2020')
    plt.xlim(xmin=0,xmax = 365)
    plt.axvline(x=365,linewidth=1, color='k')
    #plt.text(365,50,'2020',rotation=90)
    sns.set_style("ticks")
    sns.despine()
    plt.savefig('Imagenes/2020Magnitud.png', bbox_inches='tight')
    plt.show()

#Figura 3
if(False):
#Histogramas por magnitud separados. 
    #Listas para almacenar elementos
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
            
            
    fig, axs = plt.subplots(2, 2)
    fig.suptitle('Actividad sísmica semanal por magnitud 2020')
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
    plt.savefig('Imagenes/2020Magnitud2.png', bbox_inches='tight')
    fig.tight_layout()

#Figura 4
if(False):
    #Histograma con distribución de sismos
    plt.figure(3)
    plt.hist(MesDias, bins=12,color='#F93C14',alpha=0.8, rwidth=1.0,density=False, ec="k")
    #plt.grid(axis='y', color='k', linestyle='-', linewidth=1)
    plt.xlabel('Mes del año',fontsize=12)
    plt.ylabel('Cantidad de sismos',fontsize=12)
    plt.grid(axis='y', alpha=0.75)
    plt.title('Actividad sísmica mensual 2020')
    plt.xlim(xmin=0,xmax = 11)
    plt.locator_params(axis='y', integer=True)
    sns.set_style("ticks")
    plt.savefig('Imagenes/2020ActividadM.png', bbox_inches='tight')
    sns.despine()
    plt.show()
  
#Figura 5
if(False):
    #Histograma con distribución de hora
    plt.figure(3)
    plt.hist(HourD, bins=24,color='#73F914',alpha=0.8, rwidth=1.0,density=False, ec="k")
    #plt.grid(axis='y', color='k', linestyle='-', linewidth=1)
    plt.xlabel('Hora del día (UTC)',fontsize=12)
    plt.ylabel('Cantidad de sismos',fontsize=12)
    plt.grid(axis='y', alpha=0.75)
    plt.title('Actividad sísmica por hora 2020')
    plt.xlim(xmin=0,xmax = 25)
    plt.xticks(np.arange(-1, 24, 2.0), ha='left', rotation=20)
    #plt.set_xticklabels(labels, rotation=0, ha='center', minor=False)
    #plt.locator_params(axis='y', integer=True)
    sns.set_style("ticks")
    sns.despine()
    plt.savefig('Imagenes/2020ActividadPH.png', bbox_inches='tight')
    plt.show()
    
#Figura 6
if(False):
    #Histograma con distribución de sismos
    plt.figure(1)
    plt.hist(NumDias, bins=max(NumDias),color='#18D204',alpha=0.7, rwidth=1.0,
                           cumulative=True)
    #plt.grid(axis='y', color='k', linestyle='-', linewidth=1)
    plt.xlabel('Número de día del año')
    plt.ylabel('Cantidad de sismos')
    plt.title('Actividad sísmica acumulada 2020')
    plt.xlim(xmin=0,xmax = 365)
    plt.axvline(x=365,linewidth=1, color='k')
    #plt.text(365,50,'2020',rotation=90)
    sns.set_style("ticks")
    sns.despine()
    plt.savefig('Imagenes/2020ActividadA.png', bbox_inches='tight')
    plt.show()
    
# plt.figure(4)
# m01, m12, m23, m34 = [],[],[],[]
# for a,b,c,d in zip(mag01,mag12,mag23,mag34):
#     m01.append(100*a/(a+b+c+d))
#     m12.append(100*b/(a+b+c+d))
#     m23.append(100*c/(a+b+c+d))
#     m34.append(100*d/(a+b+c+d))
    
# Y = (m01,m12,m23,m34)    
# X = list(range(0,max(NumDias)))
# pal = ["#9b59b6", "#e74c3c", "#34495e", "#2ecc71"]
# plt.stackplot(X,m01)

