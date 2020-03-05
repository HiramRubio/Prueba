#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 05:00:15 2020

@author: Steven Rubio
"""


import time
from pointInside import *
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import numpy as np
import pandas as pd
#-------------------------------------------------
#Solo creamos plots que luego vamos a llenar 
fig     = plt.figure()
ax      = fig.add_subplot(111)
#Creamos nuestro mapa, entre los argumentos se encuentran: La calidad, proyeccion
#Resolucion, centro y limites
#Leemos los datos y delimitamos los limites de nuestro mapa
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

#Definimos los nombres de las zonas y el color que le queremos asignar a cada una
Zonas = ['G1','S1','G2-S2','S3','G3','G4','G5-S4-H1','G6','G8']
Colors = ['b','w','r','c','m','y','k','g','#cc66ff']
patches3 = []

#Tiempo 0 de ejecucion del programa
t = time.perf_counter() 
#Creamos la lista de los datos del nuevo csv
n_dat = []
#Recorremos todas las shapes de ej3, estas son las zonas sismogenicas de GT
for info, shape in zip(map.ej3_info, map.ej3):
    #Hacemos un ciclo para corroborar si un sismo esta en cada zona
    for j in range(len(Zonas)):
        if info['ZONA'] == Zonas[j]:
            x, y = zip(*shape)
        ax.plot(x, y, color='k') 
        for i in range(len(x)):
            patches3.append((x[i],y[i]))
            
        #Esta lista nos servira para eliminar los sismos  ya clasificados
        rm = []
        if(len(dfs)>0):
            #Recorremos todo el listado de sismos
            for i in range(len(dfs)):
                xpo = dfs[' lon'][i]
                ypo = dfs[' lat'][i]
                xpt,ypt = map(xpo,ypo)
                testP = (xpt,ypt)
                #Si las coordenadas del punto están dentro de la Zona a prueba
                #Se entra a este if
                if (is_inside_sm(patches3,testP)):
                    ax.plot(xpt,ypt,'o',color =Colors[j])
                    var = dfs[' folder'][i]
                    #Adjuntamos la data de interes y el indice que vamos a eliminar
                    n_dat.append((xpo,ypo,var,j))
                    rm.append(dfs.index[i])
            #Eliminamos los sismos ya clasificados y reiniciamos el index de nuestro archivo
            dfs.drop(rm,inplace =True)   
            dfs.reset_index(drop=True, inplace=True)
            
        patches3 = []
        
#Aqui estamos asignando la denominacion SC = Sin clasificar a todos los mismos
#Que no pertenecen a las zonas sismogenicas de GT
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

#Verificamos que todos los sismos se encuentren clasificados            
print("Longitud: ",len(dfs))
#Mostramos el tiempo de ejecucion
print("Execution time: " + str(time.perf_counter() - t)) 

#Creamos un nuevo csv con la informacion que necesitamos
dfs_n = pd.DataFrame(n_dat,columns=['lon', 'lat', 'folder','Zona'])
dfs_n.to_csv('Data/Anual2019_M.csv',index=True)
#Mostramos la data y las regiones
plt.show()