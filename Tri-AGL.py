# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 23:23:45 2020

@author: Steven Rubio

Programa que buscar determinar que tan "triangulable" podría ser un evento en 
base a donde se encuentran las estaciones
"""

import matplotlib.pyplot as plt
import numpy as np

#Creación del mapa y el Grid
Est = [(2,1,6),(1,6,4)]

x = np.linspace(0.0, 10.0)
y = np.linspace(0.0, 10.0)


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
#print(data)
        
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
with open("Data/2020-04-07-1102/20200981102.site", 'r') as f:
    for i in f:
        #Filtramos los datos que nos interesan de origin
        a = str(i[0:45])
        a = a.split()
        #Quitamos la U y todos los arrivos 'del'
        if(a[2]=='-1' and a[0] in ListPS):
            #Almacenamos: Nombre, Lat, lon, Dis (distancia al epicentro)
            text3.append((a[0],a[3],a[4],0.0))
            
print(text3)

plt.plot(Est[0],Est[1], 'o')
plt.show()