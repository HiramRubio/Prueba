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
prof = dfs[' prof']
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
if(False):
    #Histograma con distribución de sismos
    fig = plt.figure(1)
    n, bins, patches = plt.hist(NumDias, bins=semanas,color='#0504aa',alpha=0.7, rwidth=0.85)
    #plt.grid(axis='y', color='k', linestyle='-', linewidth=1)
    plt.xlabel('Día del año')
    plt.ylabel('Cantidad de sismos')
    plt.title('Actividad sísmica semanal 2020')
    plt.xlim(xmin=0,xmax = 365)
    plt.xticks([1,32,61,92,122,153,183,214,245,275,306,336], 
               ('01-01', '02-01','03-01','04-01','05-01','06-01','07-01','08-01',
                '09-01','10-01','11-01','12-01'))
    plt.xticks(rotation=60)
    plt.axvline(x=365,linewidth=1, color='k')
    #plt.text(365,50,'2020',rotation=90)
    sns.set_style("ticks")
    sns.despine()
    plt.savefig('Imagenes/Anual2020/2020Actividad.png', bbox_inches='tight')
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
             alpha=0.7, rwidth=0.85,label=nombres,density=False,cumulative=True)
    plt.legend(prop={'size': 10})
    #plt.grid(axis='y', color='k', linestyle='-', linewidth=1)
    plt.xlabel('Número de día del año')
    plt.ylabel('Cantidad de sismos')
    plt.title('Actividad sísmica semanal por magnitud 2020')
    plt.xlim(xmin=0,xmax = 365)
    plt.axvline(x=365,linewidth=1, color='k')
    #plt.text(365,50,'2020',rotation=90)
    plt.xticks([1,32,61,92,122,153,183,214,245,275,306,336], 
               ('01-01', '02-01','03-01','04-01','05-01','06-01','07-01','08-01',
                '09-01','10-01','11-01','12-01'))
    plt.xticks(rotation=60)
    sns.set_style("ticks")
    sns.despine()
    plt.savefig('Imagenes/Anual2020/2020MagnitudA.png', bbox_inches='tight')
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
    ####
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
    plt.savefig('Imagenes/Anual2020/2020Magnitud2.png', bbox_inches='tight')
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
    plt.savefig('Imagenes/Anual2020/2020ActividadM.png', bbox_inches='tight')
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
    plt.xticks(np.arange(0, 24, 2.0), ha='left', rotation=20)
    #plt.set_xticklabels(labels, rotation=0, ha='center', minor=False)
    #plt.locator_params(axis='y', integer=True)
    sns.set_style("ticks")
    sns.despine()
    plt.savefig('Imagenes/Anual2020/2020ActividadPH.png', bbox_inches='tight')
    plt.show()
    
#Figura 6
if(False):
    #Histograma con distribución de sismos
    plt.figure(4)
    plt.hist(NumDias, bins=max(NumDias),color='#4CF24C',alpha=0.9, rwidth=1.0,
                           cumulative=True)
    #plt.grid(axis='y', color='k', linestyle='-', linewidth=1)
    plt.xlabel('Mes-día')
    plt.ylabel('Cantidad de sismos')
    plt.title('Actividad sísmica acumulada 2020')
    plt.xlim(xmin=0,xmax = 365)
    plt.axvline(x=365,linewidth=1, color='k')
    plt.xticks([1,32,61,92,122,153,183,214,245,275,306,336], 
               ('01-01', '02-01','03-01','04-01','05-01','06-01','07-01','08-01',
                '09-01','10-01','11-01','12-01'))
    plt.xticks(rotation=60)
    #plt.text(365,50,'2020',rotation=90)
    sns.set_style("ticks")
    sns.despine()
    plt.savefig('Imagenes/Anual2020/2020ActividadA.png', bbox_inches='tight')
    plt.show()
    
#Figura 7
if(False):
    #Histograma con distribución de sismos por magnitud
    fig, ax = plt.subplots(figsize= (8,6))
    
    #Listas para almacenar elementos
    mag02 = []
    mag23 = []
    mag34 = []
    mag45 = []
    mag56 = []
    mag69 = []
    
    #Clasificacion por rangos
    for evento, mag in zip(folders,mag):
        if mag<= 2.0: 
            mag02.append(DayNumer2020(evento))
        if mag<= 3.0 and mag>2.0:
            mag23.append(DayNumer2020(evento))
        if mag<= 4.0 and mag >3.0:
            mag34.append(DayNumer2020(evento))
        if mag<= 5.0 and mag >4.0:
            mag45.append(DayNumer2020(evento))
        if mag<= 6.0 and mag >5.0:
            mag56.append(DayNumer2020(evento))
        if mag >6.0:
            mag69.append(DayNumer2020(evento))
    ##
    xvals = ['(0, 2.0]','(2.0, 3.0]','(3.0, 4.0]','(4.0, 5.0]','(5.0, 6.0]','(6.0, 7.52] ']
    yvals = [len(mag02),len(mag23),len(mag34),len(mag45),len(mag56),len(mag69)]
    # Create labels
    label = [f"n = {len(mag02)}",f"n = {len(mag23)}",f"n = {len(mag34)}",f"n = {len(mag45)}",f"n = {len(mag56)}",f"n = {len(mag69)}" ]
    ax.bar( xvals, yvals, width = 0.95 , edgecolor = 'black') 
    #plt.grid(axis='y', color='k', linestyle='-', linewidth=1)
    plt.xlabel('Magnitud (Ml)')
    plt.ylabel('Cantidad de sismos')
    plt.title('Actividad sísmica 2020')
    plt.xticks(rotation=30)
    #Text
    for i in range(len(label)):
        plt.text(xvals[i],yvals[i]+5.0, s = label[i], size = 10, style='oblique')
    #Styles   
    sns.set_style("ticks")
    sns.despine()
    plt.savefig('Imagenes/Anual2020/2020ActividadxM.png', bbox_inches='tight')
    plt.show()
    
#Figura 8
if(True):
    #Histograma con distribución de sismos por magnitud
    fig, ax = plt.subplots(figsize= (8,6))
    
    #Listas para almacenar elementos
    #10, 30, 70, 150, >
    prof1 = []
    prof2 = []
    prof3 = []
    prof4 = []
    prof5 = []
    
    #Clasificacion por profundidad
    for evento, prof in zip(folders,prof):
        if prof<= 10.0: 
            prof1.append(DayNumer2020(evento))
        if prof<= 30.0 and prof> 10.0:
            prof2.append(DayNumer2020(evento))
        if prof<= 70.0 and prof> 30.0:
            prof3.append(DayNumer2020(evento))
        if prof<= 150.0 and prof> 70.0:
            prof4.append(DayNumer2020(evento))
        if prof> 150.0:
            prof5.append(DayNumer2020(evento))
    ##
    xvals = ['(0, 10]','(10, 30]','(30, 70]','(70, 150]','(150, 250]']
    yvals = [len(prof1),len(prof2),len(prof3),len(prof4),len(prof5)]
    # Create labels
    label = [f"n = {len(prof1)}",f"n = {len(prof2)}",f"n = {len(prof3)}",f"n = {len(prof4)}",f"n = {len(prof5)}"]
    ax.bar( xvals, yvals, width = 0.95 , edgecolor = 'black', color = '#1341BA') 
    #plt.grid(axis='y', color='k', linestyle='-', linewidth=1)
    plt.xlabel('Profundidad (Km)')
    plt.ylabel('Cantidad de sismos')
    plt.title('Actividad sísmica 2020')
    plt.xticks(rotation=0)
    #Text
    for i in range(len(label)):
        plt.text(xvals[i],yvals[i]+5.0, s = label[i], size = 10, style='oblique')
    #Styles   
    sns.set_style("ticks")
    sns.despine()
    plt.savefig('Imagenes/Anual2020/2020ActividadxP.png', bbox_inches='tight')
    plt.show()