#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 05:00:15 2020

@author: Steven Rubio
Leer sismos de nuestra base de datos y determinar su region Sismogenetica
"""


import time
from pointInside import *
from datetime import datetime, date, timedelta
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import numpy as np
import pandas as pd
from DetMun import Det_Mun


def dia(fecha):
    '''
    Argumento de la funcion AAAA-MM-DD
    
    Calcula el numero del dia en el year
    '''
    year = int(fecha[:4]) #Cambia la variable de str a int
    mes = int(fecha[5:7])
    dia = int(fecha[8:10])
    fecha_inicial = datetime(year,1,1) #define fecha de inicio de la cuenta
    fecha = datetime(year,mes,dia) #convierte clase datetime la fecha
    a = date.toordinal(fecha) - date.toordinal(fecha_inicial) #hace la restay lo convierte a numero ordinal
    return str(a+1).zfill(3)

#-------------------------------------------------
#Solo creamos plots que luego vamos a llenar 
fig     = plt.figure()
ax      = fig.add_subplot(111)
#Creamos nuestro mapa, entre los argumentos se encuentran: La calidad, proyeccion
#Resolucion, centro y limites
#Leemos los datos y delimitamos los limites de nuestro mapa
dfs = pd.read_csv('Data/Informe3.csv')
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
Colors = ['b','w','r','g','m','y','#996633','#ff9933','#cc66ff']
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
                utf = dfs['fyh_utc'][i]
                #utf_0 = dia(utf)
                utf_0 = utf
                #if(utf_0[0]=='0'):
                #    utf_0=utf_0[1:]
                xpt,ypt = map(xpo,ypo)
                testP = (xpt,ypt)
                #Si las coordenadas del punto están dentro de la Zona a prueba
                #Se entra a este if
                if (is_inside_sm(patches3,testP)):
                    ax.plot(xpt,ypt,'o',color =Colors[j])
                    var = dfs[' folder'][i]
                    prof = dfs[' prof'][i]
                    if(prof<16.4 and prof >0):
                        z2 = 'Superficial'
                    elif(prof<38.7 and prof >=16.4):
                        z2 = 'Intra 1'
                    elif(prof<97.3 and prof >=38.7):
                        z2 = 'Intra 2'
                    elif(prof>97.3 and prof <500):
                        z2 = 'Profundo'
                    else:
                        z2 = 'NA'
                    mag = dfs[' ml'][i]
                    #mun = Det_Mun(xpo,ypo)
                    #Adjuntamos la data de interes y el indice que vamos a eliminar
                    n_dat.append((xpo,ypo,utf_0,var,Zonas[j],prof,z2,mag))
                    rm.append(dfs.index[i])
            #Eliminamos los sismos ya clasificados y reiniciamos el index de nuestro archivo
            dfs.drop(rm,inplace =True)   
            dfs.reset_index(drop=True, inplace=True)
            
        patches3 = []
        
#Aqui estamos asignando la denominacion SC = Sin clasificar a los simos
#Que no pertenecen a las zonas sismogenicas de GT y que no se encuentran en una
#Region de nuestro interes
if(len(dfs)>0):
    rm = []
    for i in range(len(dfs)):
        region = 'SC'
        color = '#666666'
        xpo = dfs[' lon'][i]
        ypo = dfs[' lat'][i]
        utf = dfs['fyh_utc'][i]
        mag = dfs[' ml'][i]
        prof = dfs[' prof'][i]
        
        #Aproximación sobre regiones de profundidad
        if(prof<15 and prof >0):
            z2 = 'Superficial'
        elif(prof<65 and prof >=15):
            z2 = 'Intra 1'
        elif(prof<150 and prof >=65):
            z2 = 'Intra 2'
        elif(prof>150 and prof <500):
            z2 = 'Profundo'
        else:
            z2 = 'NA'
        #Mapeo a coordenadas locales
        xpt,ypt = map(xpo,ypo)
        
        #Regiones extras (No Sismogenéticas)
        if(xpt<445000 and ypt<470000 and region =='SC'):     
            color ='#0DFBF2'
            region = 'MexicoCosta'
            
        if(xpt<240000 and ypt<520000 and region =='SC'):     
            color ='#0DFBF2'
            region = 'MexicoCosta'
            
        if(xpt<445000 and ypt>470000 and region =='SC'):     
            color ='#FB20C6'
            region = 'MexicoSuperior'
            
        if(ypt<445000 and ypt>240000 and xpt>880000 and region =='SC'):     
            color ='#E60DFB'
            region = 'HondurasLejano'  
            
        if(xpt>775000 and ypt<200000 and region =='SC'):     
            color ='#B0FA04'
            region = 'SalvadorLejano'                 
            
        ax.plot(xpt,ypt,'o',color =color)
        var = dfs[' folder'][i]
        #print(xpo,ypo,var,j)
        n_dat.append((xpo,ypo,utf,var,region,prof,z2,mag))
        rm.append(dfs.index[i])      
    dfs.drop(rm,inplace =True)             

#Verificamos que todos los sismos se encuentren clasificados            
print("Longitud: ",len(dfs))
#Mostramos el tiempo de ejecucion
print("Execution time: " + str(time.perf_counter() - t)) 

#Creamos un nuevo csv con la informacion que necesitamos
dfs_n = pd.DataFrame(n_dat,columns=['lon', 'lat','time','folder','Zona','prof','Zona2','ml'])
dfs_n.to_csv('Data/Informe3A.csv',index=True)
#Mostramos la data y las regiones
plt.show()