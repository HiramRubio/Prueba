# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 23:23:45 2020

@author: Steven Rubio

Programa que buscar determinar que tan "triangulable" podría ser un evento en 
base a donde se encuentran las estaciones
"""
from pointInside import is_inside_sm
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
import random
#import shapely.geometry as sg
#import descartes
import sympy
import pandas as pd

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
data = text[0].split("  ",4)
#Solo guardamos los primeros 4 datos: Lat, lon, prof, tiempo
#El tiempo se encuentra en un formato conocido como Unix Epoch
data = data[0:4]
#print("Datos Origen: ")
#Coordenadas locales del origen
xpt,ypt = m(float(data[1]),float(data[0]))


text2 = []
#Abrimos un evento
with open(str2+".arrival", 'r') as f: 
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
with open(str2+".site", 'r') as f:
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
                    
#Variable para ejecutar un ciclo de localizaciones
val = True
lol = 0
Fails = 0
#[0, 3, 6]
#[6, 11, 3]
#[6, 2, 3]
#[6, 1, 3]
while(val):    
    #print(lol)
    lol=lol+1
    if(lol==1): val=False
    #n = [12,1,11]   #Sol erronea pero en rango
    #n = [11,2,7]   #Sol erronea pero en rango
    #n = [2,11,4] 
    n = random.sample(range(len(Estx)),3)
   
    #Calculamos distancia euclidiana entre las estaciones seleccionadas
    d_ab = np.linalg.norm(np.array((Estx[n[0]],Esty[n[0]]))-np.array((Estx[n[1]],Esty[n[1]])))
    d_ac = np.linalg.norm(np.array((Estx[n[0]],Esty[n[0]]))-np.array((Estx[n[2]],Esty[n[2]]))) 
    d_bc = np.linalg.norm(np.array((Estx[n[1]],Esty[n[1]]))-np.array((Estx[n[2]],Esty[n[2]])))    
    #Validamos si los circulos de las 3 estaciones se intersectan y que sus centros 
    #no se encuentren dentro de otro circulo
    xa = (text3[n[0]][3]+text3[n[1]][3])-d_ab
    xb = (text3[n[0]][3]+text3[n[2]][3])-d_ac
    xc = (text3[n[1]][3]+text3[n[2]][3])-d_bc
    #Valor para ver cantidad de casos
    Casos = 0
    if( d_ab - text3[n[0]][3] >0): Casos=Casos+1
    if( d_ac - text3[n[0]][3] >0): Casos=Casos+1
    if( d_bc - text3[n[1]][3] >0): Casos=Casos+1
    if( d_ab - text3[n[1]][3] >0): Casos=Casos+1
    if( d_bc - text3[n[2]][3] >0): Casos=Casos+1
    if( d_ac - text3[n[2]][3] >0): Casos=Casos+1
    
    if(Casos==6):
            Mensaje = "Posible solucion correcta (Mejor caso)"
            val = False
    elif(Casos==5 or Casos == 4): 
        Mensaje = "Posible solucion (Estaciones Alineadas o muy cercanas)" 
    else:   
        Mensaje = "Triangulación no confiable"

    #print("Grado de la solución: "+str(Casos))

    #Buscamos la solución numerica de donde se intersectan los circulos
    x, y = sympy.symbols("x y", real=True)
    
    h1,k1,r1 = Estx[n[0]],Esty[n[0]],text3[n[0]][3]
    h2,k2,r2 = Estx[n[1]],Esty[n[1]],text3[n[1]][3]
    h3,k3,r3 = Estx[n[2]],Esty[n[2]],text3[n[2]][3]
    
    #Resolvemos las ecuaciones para determinar donde se intersectan los circulos                         
    eq1 = sympy.Eq((x-h1)**2 + (y-k1)**2, r1**2)
    eq2 = sympy.Eq((x-h2)**2 + (y-k2)**2, r2**2)
    eq3 = sympy.Eq((x-h3)**2 + (y-k3)**2, r3**2)
    sol1 = sympy.solve([eq1, eq2])
    sol2 = sympy.solve([eq1, eq3])
    sol3 = sympy.solve([eq2, eq3])
    
    #Posibles soluciones
    S1 = []
    S1.append((sol1[0][x],sol1[0][y]))
    S1.append((sol1[1][x],sol1[1][y]))
    S2 = []
    S2.append((sol2[0][x],sol2[0][y]))
    S2.append((sol2[1][x],sol2[1][y]))
    S3 = []
    S3.append((sol3[0][x],sol3[0][y]))
    S3.append((sol3[1][x],sol3[1][y]))
    
    #Determinamos las soluciones que están cerca
    SF = []
    SFx = []
    SFy = []
    CV = 0.0
    k=0
    for a in S1:
        for b in S2:
            for c in S3:
                k = k+1
                NV = abs(a[0]-b[0])+abs(a[0]-c[0])+abs(c[0]-b[0])
                print(k,": ",NV)
                if(CV==0.0):
                    CV = NV
                    SF.append((a[0],a[1]))
                    SF.append((b[0],b[1]))
                    SF.append((c[0],c[1]))
                    SFx.append(a[0])
                    SFx.append(b[0])
                    SFx.append(c[0])
                    SFy.append(a[1])
                    SFy.append(b[1])
                    SFy.append(c[1])
                if(NV<CV):
                    SF = [(a[0],a[1]),(b[0],b[1]),(c[0],c[1])]
                    SFx = [a[0],b[0],c[0]]
                    SFy = [a[1],b[1],c[1]]
                    CV = NV
      
    #Hacemos un promedio de las soluciones y determinamos el error
    patches3 = []
    for i in range(len(SFx)):
            patches3.append((SFx[i],SFy[i]))
    testP = (xpt,ypt)
    
    if (is_inside_sm(patches3,testP)!=0):  menj3 = ("Inside")
    else:   menj3 = ("Outside")
        
        
    SFxm = (SFx[0]+SFx[1]+SFx[2])/3
    SFxep = max(SFx) 
    SFxen = min(SFx)
    
    SFym = (SFy[0]+SFy[1]+SFy[2])/3
    SFyep = max(SFy)
    SFyen = min(SFy)
    
    lonF,latF = m( SFxm,SFym,True)
    erxp,eryp = m( SFxep,SFyep,True)
    erxn,eryn = m( SFxen,SFyen,True)
    
    #Validacion de la solución
    if(-erxn+lonF<0.01 and erxp-lonF<0.01 and -eryn+latF<0.01 and eryp-latF<0.01):
        #print("Acierto en la solucion")
        mensj2 = ", Acierto"
        val2 = True
    else: 
        #print("Solucion no correcta")
        mensj2 = ", Sol. Erronea"+str(n)
        Fails = Fails + 1
        val2 = False
    
    print("Solucion Antelope: "+data[0]+", "+data[1])
    print(str(lol)+" Grado: "+str(Casos)+", Solucion Programa > Lat: "+str(latF)+", Lon: "+str(lonF)+mensj2)
    print("Error lon: -"+str(-erxn+lonF)+" / +"+str(erxp-lonF))
    print("Error Lat: -"+str(-eryn+latF)+" / +"+str(eryp-latF))
    
    #Ploteamos los puntos
    # for a in SF:    
    #     plt.plot(a[0],a[1],marker='.',color='y')
     
    #Agregamos datos a .csv
    n_dat.append((name,text3[n[0]][0],text3[n[1]][0],text3[n[2]][0],Casos,latF,lonF,val2,menj3))   
        
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


#Ploteamos el origen
plt.plot(xpt,ypt,marker='*',color='m')    
#Ploteamos las estaciones
print("Estaciones Utilizadas para triangulazión")
for i in range(len(Estx)):
    if(i in n):
        CP = plt.Circle((Estx[i],Esty[i]),radius=text3[i][3],color='g',fill=False)
        ax.add_artist(CP)
        print("Nombre: "+ str(text3[i][0])+", Coordenadas: ("+str(text3[i][1])+","+str(text3[i][2])+")")
        plt.plot(Estx[i],Esty[i],marker='^',color='g')
    else:
        plt.plot(Estx[i],Esty[i],marker='.',color='r')
        

plt.title(Mensaje)
plt.show()


coord = [[SFx[0],SFy[0]], [SFx[1],SFy[1]], [SFx[2],SFy[2]]]
coord.append(coord[0]) #repeat the first point to create a 'closed loop'

plt.figure()
xs, ys = zip(*coord) #create lists of x and y values
plt.plot(xs,ys) 
plt.plot(xpt,ypt,marker='*',color='m') 
plt.show()
#Creamos un nuevo csv con la informacion que necesitamos
dfs_n = pd.DataFrame(n_dat,columns=['Folder','Est1','Est2','Est3','Grado','Lat','Lon','Acierto','Inside'])
dfs_n.to_csv('Data/2020-05-07-0233-S2.csv',index=True)
#Titulo
#plt.title(Mensaje)
#plt.show()
