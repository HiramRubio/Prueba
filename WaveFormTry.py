# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 06:34:22 2020

@author: HRV
"""

import pandas as pd
import matplotlib.pyplot as plt
import math
import pandas as pd 
import numpy as np

homeDir = "C:/Users/HRV/Desktop/Post-U/Trabajo/Prueba/Data/Eventos/"
folder = '2019-11-13-1628'
est = pd.read_csv(homeDir+str(folder)+'_estaciones.csv')

#Funcion para generar puntos esperados de onda
def expected_wave_points(xo,yo,est):
    # ----------
    # Entradas:
    # xo,yo     = Coordenadas del evento
    # est       = Archivo .csv con datos del evento
    # ----------
    # Salidas:
    # x_e_p,y_e_p   = Coordenadas de onda esperadas
    # time_e        = Lista con los tiempos (segundos desde origen) en que se 
    #                 espera que la onda pase en cierta coordenada
    # onda_e        = Nombre de onda
    # ----------     
    
    #List to save values
    y_e_p = []
    x_e_p = []
    time_e = []
    onda_e = []
    
    #Loop para generar todos los puntos esperados
    for name,yv,xv,t,onda in zip(est['Est'],est['Lat'],est['Lon'],est['DeltaT (segundos)'],est['Onda']):
        #New point or expected point
        dx, dy = xv-xo, yv-yo
        var = 1
        #Generation of expected wave points
        while(var <= t):
            x_p = var*dx/t+xo
            y_p = var*dy/t+yo
            #Saving points
            x_e_p.append(x_p)
            y_e_p.append(y_p)
            time_e.append(var)
            onda_e.append(onda)
            #print("Expeted point ",var,": ",x_p,y_p)
            var= var+1
            
    return x_e_p, y_e_p, time_e, onda_e
    
    
x_pts,y_pts,t_pts,w_pts = expected_wave_points(-90.9683,13.6853,est) 

#Plot
fig, ax = plt.subplots(figsize=(8,8))

plot = ax.plot(-90.9683,13.6853,'s',marker='*',color='k', markersize=10,markeredgecolor = 'k')

a1, b1, ag1 = [], [], []
a2, b2, ag2 = [], [], []
for x,y,i,o in zip(x_pts,y_pts,t_pts,w_pts):
    if(i==1 and o =='P'):
        plot = ax.plot(x,y,'s',marker='.',color='r', markersize=8,markeredgecolor = 'k')
        a1.append(x)
        b1.append(y)
        ag1.append(math.degrees(math.atan2((y-13.6853),(x+90.9683))))
    if(i==3 and o =='P'):
        plot = ax.plot(x,y,'s',marker='.',color='b', markersize=8,markeredgecolor = 'k')
        a2.append(x)
        b2.append(y)
        ag2.append(math.degrees(math.atan2((y-13.6853),(x+90.9683))))
 
#Data Frame 1
data = np.array([a1,b1,ag1])
df = pd.DataFrame(data=data)
df = df.T
#Plot 
dfS = df.sort_values(by = [2])
ax.plot(dfS[0], dfS[1], 'r:o')

#Data Frame 2
data2 = np.array([a2,b2,ag2])
df2 = pd.DataFrame(data=data2)
df2 = df2.T
#Plot
dfS2 = df2.sort_values(by = [2])
ax.plot(dfS2[0], dfS2[1], 'b:o')


