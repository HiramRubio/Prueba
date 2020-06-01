# -*- coding: utf-8 -*-
"""
Created on Sun May 31 03:54:02 2020

@author: Steven Rubio
"""


# Abriendo el evento y extrañendo el origen y las Estaciones que se utilizaron para localizarlo
text = []
#Creamos la lista de los datos del nuevo csv
n_dat = []

str2 = "Data/2020-05-07-0233/20201280233"
name = "2020-05-07-0233"
#str2 = "Data/2020-04-07-1102/20200981102"
#name = "2020-04-07-1102"
with open(str2+".origin", 'r') as f:
    for i in f:
        if (i[0:4]!='-999'):
            text.append(str(i[2:]))
        #print('Verdadero Origin: ')
        #print(text)
        
#Cortamos los espacios en blanco para obtener solo la data
data = text[0].split("  ",36)
#Solo guardamos los primeros 4 datos: Lat, lon, prof, tiempo, magnitud
#El tiempo se encuentra en un formato conocido como Unix Epoch
data = (data[0],data[1],data[2],data[3],data[32])

 
text2 = []
#Abrimos un evento
with open(str2+".arrival", 'r') as f: 
    for i in f:
        #Filtramos los datos que nos interesan de origin
        a = str(i[0:75])
        a = a.split()
        #Quitamos la U y todos los arrivos 'del' o 'mL'
        if(len(a)==8 and a[7]!='del' and a[7]!='ml'):
            text2.append(a)     
            
#print(text2)
#Almacenamos la estacion y el tiempo que les tomo llegar a la onda en listas separadas            
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
with open(str2+".site", 'r') as f:
    for i in f:
        #Filtramos los datos que nos interesan de origin
        a = str(i[0:45])
        a = a.split()
        #Quitamos la U y todos los arrivos 'del'
        if(a[2]=='-1' and a[0] in ListPS):
            #Almacenamos: Nombre, Lat, lon, Dis (distancia al epicentro)
            xEs,yEs = (float(a[4]),float(a[3]))
            #Calculamos distancia euclidiana
            #dist = np.linalg.norm(np.array((xpt,ypt))-np.array((xEs,yEs)))
            dist = 0
            text3.append((a[0],a[3],a[4],dist))
            #Almacenamos las coordenadas para ploteo
            Estx.append(xEs)
            Esty.append(yEs)   