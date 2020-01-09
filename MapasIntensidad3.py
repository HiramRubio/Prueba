#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 11:26:35 2019

@author: Steven 
"""

import pandas
import matplotlib.pyplot as plt
import pyproj as proj
import numpy as np; np.random.seed(1)
from scipy.spatial import ConvexHull
from scipy.spatial import distance



def Intensidad_E(Ex,Ey,Px,Py,Esx,Esy,IE,IP):
    """
    Ex, Ey = Puntos x,y del Epicentro
    Px, Py = Puntos x,y del punto que se va a estimar
    Esx, Esy = Puntos x,y de la Estacion
    IE = Intensidad Epicentro
    IP = Intensidad Punto
    """
    a = np.array([Ex,Ey])
    b = np.array([Px,Py])
    c = np.array([Esx,Esy])

    ba = a - b
    bc = c - b
    #Distancia Epicentro
    d_ba = np.linalg.norm(ba) 
    #Distancia Punto
    d_bc = np.linalg.norm(bc)

    cosine_angle = np.dot(ba, bc) / (d_ba * d_bc)
    angle = np.arccos(cosine_angle)
    angle_d = np.degrees(angle)
    DI = IE - IP
    #print(angle_d)
    if (angle_d>155.0 and angle_d<205.0):
        I_est = IE - (d_ba/ (d_ba+d_bc) )*DI
    else: I_est = 0
    return(I_est,angle_d)


#Agregar los valores fijos de intensidad

crs_wgs = proj.Proj(init='epsg:4326')  # assuming you're using WGS84 geographic

#Erect own local flat cartesian coordinate system
#Colocamos el punto central de nuestro sistema
#En ese caso escogi la UMG
gps_lat_0 = 14.656501
gps_long_0 = -90.512975
cust = proj.Proj("+proj=aeqd +lat_0={0} +lon_0={1} +datum=WGS84 +units=m".format(gps_lat_0, gps_long_0))

#Leemos  el archivo
df = pandas.read_csv('2019-11-30-0744.csv')
#print(df)
#Nuestro array para almacenar puntos
P = []

for i in range(0,len(df)):    
    x = proj.transform(crs_wgs, cust,	df['lon'][i],df['lat'][i])
    P.append( (df['Nombre'][i],x[0],x[1],df['Intensidad'][i]) )
    
#Definimos nuestra region
xo, yf = proj.transform(crs_wgs, cust, -94.0, 19.0)
xf, yo = proj.transform(crs_wgs, cust, -87.0, 12.0)
Dx = (xo,xf)
Dy = (yo,yf)

C1 = []
C2 = []
C3 = []
#Este almacena todos los puntos 
for i in range(0,len(P)):
    C1.append(P[i][1])
    C2.append(P[i][2])
    C3.append(P[i][3])


x_Ep =C1[len(C1)-1]
y_Ep =C2[len(C1)-1]
print( "Epicentro: "+str(x_Ep)+" "+str(y_Ep) )
#Ploteamos las estaciones
plt.plot(C1,C2, 'ro', P[len(P)-1][1], P[len(P)-1][2],'go')
#Guardamos la intensidad en el epicentro
IO = P[len(P)-1][3]
#print('Distancia maxima: ',str(rmax))
#------------------------------------------

#Encerrando la data con poligonos irregulares
def encircle(x,y, ax=None, **kw):
    if not ax: ax=plt.gca()
    p = np.c_[x,y]
    hull = ConvexHull(p)
    poly = plt.Polygon(p[hull.vertices,:], **kw)
    ax.add_patch(poly)

#Encerrando la data con un elipsoide
def encircle2(x,y, ax=None, **kw):
    if not ax: ax=plt.gca()
    p = np.c_[x,y]
    #Nuestra media siempre es el epicentro
    mean = (P[len(P)-1][1], P[len(P)-1][2])
    d = p-mean
    r = np.max(np.sqrt(d[:,0]**2+d[:,1]**2 ))
    circ = plt.Circle(mean, radius=1.05*r,**kw)
    ax.add_patch(circ)

#Defino 4 regiones
h = (max(C3)-min(C3))/5
R1x = []
R1y = []
R2x = []
R2y = []
R3x = []
R3y = []
R4x = []
R4y = []
R5x = []
R5y = []

for i in range(0,len(P)):
    if C3[i]> (min(C3)):
        R1x.append(C1[i])
        R1y.append(C2[i])
        if C3[i]> (min(C3)+h):
            R2x.append(C1[i])
            R2y.append(C2[i])
            if C3[i]> (min(C3)+2*h):
                R3x.append(C1[i])
                R3y.append(C2[i])
                if C3[i]> (min(C3)+3*h):
                    R4x.append(C1[i])
                    R4y.append(C2[i])
                    if C3[i]> (min(C3)+4*h):
                        R5x.append(C1[i])
                        R5y.append(C2[i])

encircle2(R1x, R1y, ec="blue", fc="none", alpha=0.2)
encircle2(R2x, R2y, ec="green", fc="none", alpha=0.2)
encircle2(R3x, R3y, ec="yellow", fc="none", alpha=0.2)
encircle2(R4x, R4y, ec="orange", fc="none", alpha=0.2)
encircle2(R5x, R5y, ec="red", fc="gold", alpha=0.2)
plt.gca().relim()
plt.gca().autoscale_view()
#plt.show()
#------------------------------------------------------
#Ahora debemos crear otro grip y llenarlo
#Listas de los puntos x,y e intensidad
PFx = []
PFy = []
PFI = []
#Definimos el tamaño del grid
for j in range(int(Dx[0]),int(Dx[1]),2500):
    for i in range(int(Dy[0]),int(Dy[1]),2500):
        I_est = 0
        n_est = len(C1)-2
        P = []
        for io in range(n_est):
            I_x,y = Intensidad_E(C1[n_est+1],C2[n_est+1],i,j,C1[io],C2[io],IO,C3[io])
            if(I_x != 0): P.append(I_x)
            #print(I_x)
    
        if(len(P)!=0):
            I_est = sum(w for w in P)/len(P)   
            PFx.append(i)
            PFy.append(j)
            PFI.append(I_est)

#Agregando el epicentro solo como prueba
PFx.append(x_Ep)
PFy.append(y_Ep)
PFI.append(IO)
#--------------
fig,ax = plt.subplots()
ax.scatter(PFx, PFy, c=PFI, s=50)
plt.show()
