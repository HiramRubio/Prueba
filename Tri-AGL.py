# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 23:23:45 2020

@author: Steven Rubio

Programa que buscar determinar que tan "triangulable" podría ser un evento en 
base a donde se encuentran las estaciones
"""

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap

fig, ax = plt.subplots(figsize=(8,8))
Opc = False
#Nacional
m = Basemap(resolution='i', # c, l, i, h, f or None
    lat_0=14.6569, lon_0=-90.51,
    llcrnrlon=-92.93, llcrnrlat=13.15,urcrnrlon=-87.58, urcrnrlat=18.42,
    projection='tmerc')
    
m.drawmapboundary(fill_color='#46bcec')                  
m.fillcontinents(color='#f2f2f2',lake_color='#46bcec')
    
#Creación del mapa y el Grid
#Est = [(2,1,6),(1,6,4)]
#x = np.linspace(0.0, 10.0)
#y = np.linspace(0.0, 10.0)

# Abriendo el evento y extrañendo el origen y las Estaciones que se utilizaron para localizarlo
text = []
with open("Data/2020-04-07-1102/20200981102.origin", 'r') as f:
    for i in f:
        if (i[0:4]!='-999'):
            text.append(str(i[2:]))
        #print('Verdadero Origin: ')
        #print(text)
    
#Cortamos los espacios en blanco para obtener solo la data
data = text[0].split("  ",4)
#Solo guardamos los primeros 4 datos: Lat, lon, prof, tiempo
#El tiempo se encuentra en un formato conocido como Unix Epoch
data = data[0:4]
#print("Datos Origen: ")
#Coordenadas locales del origen
xpt,ypt = m(float(data[1]),float(data[0]))


text2 = []
#Abrimos un evento
with open("Data/2020-04-07-1102/20200981102.arrival", 'r') as f: 
    for i in f:
        #Filtramos los datos que nos interesan de origin
        a = str(i[0:75])
        a = a.split()
        #Quitamos la U y todos los arrivos 'del'
        if(len(a)==8 and a[7]!='del'):
            text2.append(a)
      
#print(text2)
#Almacenamos la estacion y el tiempo que le tomo llegar a la onda en listas separadas            
#Almacenamos todas las P 
ListP = []
#print("Ondas P: ")
for i in range(len(text2)):
    if(text2[i][7]=='P'):
        x = float(data[3])-float(text2[i][1])
        ListP.append((text2[i][0],x))
#        print((text2[i][0],x))

#Almacenamos todas las S
ListS = []
#print("Ondas S: ")
for i in range(len(text2)):
    if(text2[i][7]=='S'):
        x = float(data[3])-float(text2[i][1])
        ListS.append((text2[i][0],x))
#        print((text2[i][0],x))
        

#Creamos una lista con el nombre las estaciones con ondas S y P
ListPS = []
for i in range(len(ListP)):
    for j in range(len(ListS)):
        if(ListP[i][0]==ListS[j][0]): ListPS.append(ListP[i][0])


#Extramos la Lat y Lon de las estaciones con ondas P y S registradas
text3 = []
Estx = []
Esty = []
with open("Data/2020-04-07-1102/20200981102.site", 'r') as f:
    for i in f:
        #Filtramos los datos que nos interesan de origin
        a = str(i[0:45])
        a = a.split()
        #Quitamos la U y todos los arrivos 'del'
        if(a[2]=='-1' and a[0] in ListPS):
            #Almacenamos: Nombre, Lat, lon, Dis (distancia al epicentro)
            xEs,yEs = m(float(a[4]),float(a[3]))
            #Calculamos distancia euclidiana
            dist = np.linalg.norm(np.array((xpt,ypt))-np.array((xEs,yEs)))
            text3.append((a[0],a[3],a[4],dist))
            #Almacenamos las coordenadas para ploteo
            Estx.append(xEs)
            Esty.append(yEs)
                    
#print(text3)
#Ploteamos el origen
plt.plot(xpt,ypt,marker='*',color='m')
#Ploteamos las estaciones
for i in range(len(Estx)):
    plt.plot(Estx[i],Esty[i],marker='.',color='r')

#Leemos nuestra shapefile, no los activamos todos
m.readshapefile('Data/gtm/gtm_admbnda_adm0_ocha_conred_20190207', 'ej0',linewidth=1.5)
m.readshapefile('Data/gtm/gtm_admbnda_adm1_ocha_conred_20190207', 'ej1',drawbounds=True)
plt.show()