#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 05:00:15 2020

@author: Steven Rubio
"""

import sys
import copy
import time
import random

from pointInside import *

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.patches import PathPatch
import numpy as np
import pandas as pd
import time
#-------------------------------------------------
#Solo creamos plots que luego vamos a llenar 
fig     = plt.figure()
ax      = fig.add_subplot(111)
#Creamos nuestro mapa, entre los argumentos se encuentran: La calidad, proyeccion
#Resolucion, centro y limites
dfs = pd.read_csv('Data/Anual2019.csv')
#print(max(dfs[' lon']),min(dfs[' lon']))
x1,x2 = max(dfs[' lon']),min(dfs[' lon'])
#print(max(dfs[' lat']),min(dfs[' lat']))
y1,y2 = max(dfs[' lat']),min(dfs[' lat'])
map = Basemap(resolution='i', # c, l, i, h, f or None
            projection='merc', 
            lat_0=14.6569, lon_0=-90.51,
            llcrnrlon=x2+0.1, llcrnrlat=y2-0.1,urcrnrlon=x1-0.1, urcrnrlat=y1+0.1)

#Dibujamos el background de nuestro mapa
map.drawmapboundary(fill_color='#46bcec')
map.fillcontinents(color='#f2f2f2',lake_color='#46bcec')
map.drawcoastlines()

#Leemos las Shapefiles. Estas las consegui en un rincon oscuro de internet, 
#podemos generar las nuestras para pintar regiones, etc.
map.readshapefile('Data/gtm/gtm_admbnda_adm0_ocha_conred_20190207', 'ej0',linewidth=1.0)
map.readshapefile('Data/gtm/gtm_admbnda_adm1_ocha_conred_20190207', 'ej1',drawbounds=False)
map.readshapefile('Data/gtm/gtm_admbnda_adm2_ocha_conred_20190207', 'ej2',drawbounds=False)
map.readshapefile('Data/ale/ZONASSISMOMOD', 'ej3',drawbounds=True)
#print(map.ej3_info)

patches   = []
patches2 = []
#Pintamos solamente la capital
for info, shape in zip(map.ej3_info, map.ej3):
    if info['SHAPENUM'] == 3:
        patches.append( Polygon(np.array(shape), True))
        patches2.append(np.array(shape))

Zonas = ['G1','S1','G2-S2','S3','G3','G4','G5-S4-H1','G6','G8']
Colors = ['b','w','r','c','m','y','k','g','#cc66ff']
patches3 = []

t = time.perf_counter() 

n_dat = []
for info, shape in zip(map.ej3_info, map.ej3):
    for j in range(len(Zonas)):
        if info['ZONA'] == Zonas[j]:
            x, y = zip(*shape)
        ax.plot(x, y, color='k') 
        for i in range(len(x)):
            patches3.append((x[i],y[i]))
        
        rm = []
        #print(dfs)
        #print("*********************")
        #print(n_dat)
        if(len(dfs)>0):
            for i in range(len(dfs)):
                #print("Longitud: ",len(dfs))
                #print(i)
                xpo = dfs[' lon'][i]
                ypo = dfs[' lat'][i]
                xpt,ypt = map(xpo,ypo)
                testP = (xpt,ypt)
                if (is_inside_sm(patches3,testP)):
                    ax.plot(xpt,ypt,'o',color =Colors[j])
                    var = dfs[' folder'][i]
                    #print(xpo,ypo,var,j)
                    n_dat.append((xpo,ypo,var,j))
                    #print("La estacion", dfs['Name'][i], "Esta dentro de la region: ",Zonas[j]) 
                    #print(dfs.index[i-1])
                    rm.append(dfs.index[i])
                
            dfs.drop(rm,inplace =True)   
            dfs.reset_index(drop=True, inplace=True)
            
        patches3 = []

if(len(dfs)>0):
    rm = []
    for i in range(len(dfs)):
        xpo = dfs[' lon'][i]
        ypo = dfs[' lat'][i]
        xpt,ypt = map(xpo,ypo)
        ax.plot(xpt,ypt,'o',color ='k')
        var = dfs[' folder'][i]
        #print(xpo,ypo,var,j)
        n_dat.append((xpo,ypo,var,'SC'))
        rm.append(dfs.index[i])      
    dfs.drop(rm,inplace =True)             
                
print("Longitud: ",len(dfs))
print("Execution time: " + str(time.perf_counter() - t)) 

#print(n_dat)
dfs_n = pd.DataFrame(n_dat,columns=['lon', 'lat', 'folder','Zona'])
#print(dfs_n)
dfs_n.to_csv('Data/Anual2019_M.csv',index=True)

plt.show()