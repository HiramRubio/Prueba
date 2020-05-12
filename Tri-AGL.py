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
import random
import shapely.geometry as sg
import descartes

fig, ax = plt.subplots(figsize=(8,8))
Opc = False
#Nacional
m = Basemap(resolution='i', # c, l, i, h, f or None
    lat_0=14.6569, lon_0=-90.51,
    llcrnrlon=-92.93, llcrnrlat=13.15,urcrnrlon=-87.58, urcrnrlat=18.42,
    projection='tmerc')
    
m.drawmapboundary(fill_color='#46bcec')                  
m.fillcontinents(color='#f2f2f2',lake_color='#46bcec')
#Leemos nuestra shapefile, no los activamos todos
m.readshapefile('Data/gtm/gtm_admbnda_adm0_ocha_conred_20190207', 'ej0',linewidth=1.5)
m.readshapefile('Data/gtm/gtm_admbnda_adm1_ocha_conred_20190207', 'ej1',drawbounds=True)
   
#Creación del mapa y el Grid
#Est = [(2,1,6),(1,6,4)]
#x = np.linspace(0.0, 10.0)
#y = np.linspace(0.0, 10.0)

# Abriendo el evento y extrañendo el origen y las Estaciones que se utilizaron para localizarlo
text = []
with open("Data/2020-05-07-0233/20201280233.origin", 'r') as f:
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
with open("Data/2020-05-07-0233/20201280233.arrival", 'r') as f: 
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
with open("Data/2020-05-07-0233/20201280233.site", 'r') as f:
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

n = random.sample(range(len(Estx)),3)
n = [7,8,0]    #Un vector random que ayuda bueno
#n = [11,7,1]   #Un vector random debil
print(n)
#Calculamos distancia euclidiana entre las estaciones seleccionadas
d_ab = np.linalg.norm(np.array((Estx[n[0]],Esty[n[0]]))-np.array((Estx[n[1]],Esty[n[1]])))
d_ac = np.linalg.norm(np.array((Estx[n[0]],Esty[n[0]]))-np.array((Estx[n[2]],Esty[n[2]]))) 
d_bc = np.linalg.norm(np.array((Estx[n[1]],Esty[n[1]]))-np.array((Estx[n[2]],Esty[n[2]])))    

#Validamos si los circulos de las 3 estaciones se intersectan y que sus centros 
#no se encuentren dentro de otro circulo
xa = (text3[n[0]][3]+text3[n[1]][3])-d_ab
xb = (text3[n[0]][3]+text3[n[2]][3])-d_ac
xc = (text3[n[1]][3]+text3[n[2]][3])-d_bc
xa2 = d_ab - text3[n[0]][3] 
xb2 = d_ac - text3[n[0]][3] 
xc2 = d_bc - text3[n[2]][3] 
val = True
if(xa>0 and xb>0 and xc>0): 
    if(xa2>0 and xb2>0 and xc2>0):  Mensaje = "Posible solucion correcta"
    elif( (xa2>0 and xb2>0) or (xb2>0 and xc2>0) or (xc2>0 and xc2>0)): 
            Mensaje = "Posible solucion (Estaciones ALineadas o muy cercanas)" 
    else:   Mensaje = "Triangulación no suficientemente confiable"
else:   
    Mensaje = "Triangulación no confiable"
    val = False
    


print("Estaciones Utilizadas para triangulazión")
for i in range(len(Estx)):
    if(i in n):
        CP = plt.Circle((Estx[i],Esty[i]),radius=text3[i][3],color='g',fill=False)
        ax.add_artist(CP)
        print("Nombre: "+ str(text3[i][0])+" Coordenadas: ("+str(text3[i][1])+","+str(text3[i][2])+")")
        plt.plot(Estx[i],Esty[i],marker='^',color='g')
    else:
        plt.plot(Estx[i],Esty[i],marker='.',color='r')


#Vemos el area que intersecta las 3 partes

# a = sg.Point(Estx[n[0]],Esty[n[0]]).buffer(text3[n[0]][3])
# b = sg.Point(Estx[n[1]],Esty[n[1]]).buffer(text3[n[1]][3])
# c = sg.Point(Estx[n[2]],Esty[n[2]]).buffer(text3[n[2]][3])
# abc = a.intersection(b)
# abc = abc.intersection(c)
# ab = a.intersection(b)
# ac = a.intersection(c)
# bc = b.intersection(c)
# ax.add_patch(descartes.PolygonPatch(ab, fc='g', ec='k', alpha=0.2))
# ax.add_patch(descartes.PolygonPatch(ac, fc='b', ec='k', alpha=0.2))
# ax.add_patch(descartes.PolygonPatch(bc, fc='y', ec='k', alpha=0.2))
# ax.add_patch(descartes.PolygonPatch(abc, fc='r', ec='k', alpha=0.2))
#Titulo
plt.title(Mensaje)
plt.show()