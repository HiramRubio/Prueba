#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 12:05:27 2020

@author: Steven Rubio
"""
import pandas
import matplotlib.pyplot as plt
import pyproj as proj
import numpy as np; np.random.seed(1)
from pandas import DataFrame

#Proyección 
crs_wgs = proj.Proj(init='epsg:4326')  # assuming you're using WGS84 geographic
#Erect own local flat cartesian coordinate system
#Colocamos el punto central de nuestro sistema
#En ese caso escogi la UMG
gps_lat_0 = 14.656501
gps_long_0 = -90.512975
cust = proj.Proj("+proj=aeqd +lat_0={0} +lon_0={1} +datum=WGS84 +units=m".format(gps_lat_0, gps_long_0))

#Leemos  el archivo
df = pandas.read_csv('eventos/intensidad3.csv')
#print(df)
#Nuestro array para almacenar puntos ya convertidos
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
#Este almacena todos los puntos y las intensidades
for i in range(0,len(P)):
    C1.append(P[i][1])
    C2.append(P[i][2])
    C3.append(P[i][3])

#Guardamos la info del epicentro
x_Ep =C1[len(C1)-1]
y_Ep =C2[len(C1)-1]
print( "Epicentro: "+str(x_Ep)+" "+str(y_Ep) )
#Ploteamos las estaciones
plt.plot(C1,C2, 'ro', P[len(P)-1][1], P[len(P)-1][2],'go')
#Guardamos la intensidad 
IO = P[len(P)-1][3]
#Usamos otro punto para el calculo de angulo 
x_ref = x_Ep + 10000
#Calculamos el angulo y lo que decae en intensidad
n_est = len(C1)-1
P_Angle = [None] * (n_est-1)
P_DI = [None] * (n_est-1)
P_Dist= [None] * (n_est-1)

for i in range(n_est-1):
    """
    a = Puntos x,y del Epicentro corrido
    b = Puntos x,y del Epicentro
    c = Puntos x,y de la Estacion
    """
    a = np.array([x_ref,y_Ep])
    b = np.array([x_Ep,y_Ep])
    c = np.array([C1[i],C2[i]])
    ba = a - b
    bc = c - b
    #Distancia Epicentro a Punto
    d_ba = np.linalg.norm(ba) 
    #Distancia Estacion a Epicentro
    d_bc = np.linalg.norm(bc)
    #----------#
    cosine_angle = np.dot(ba, bc) / (d_ba * d_bc)
    angle = np.arccos(cosine_angle)
    angle_d = np.degrees(angle)
    #---------------#
    DI = IO - C3[i]
    P_Angle[i] = angle_d
    P_DI[i] = DI
    P_Dist[i] = d_bc
#print(str(P_Angle[2])+" "+str(P_DI[2])+" "+str(P_Dist[2]))

data = {'Angle': P_Angle, 
        'DI': P_DI,
        "Distance": P_Dist
        }

df = DataFrame(data, columns= ['Angle',"DI","Distance"])
export_csv = df.to_csv ('Modelo/Data_intensidad3.csv', index = None, header=True) #Don't forget to add '.csv' at the end of the path
#print (df)
print("Done!")
