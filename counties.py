from __future__ import (absolute_import, division, print_function)

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import pandas as pd
import matplotlib as mpl
import matplotlib.colors as mcolors
import  matplotlib.cm as cm
import numpy as np; np.random.seed(1)
import math

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
    #Distancia Epicentro a Punto
    d_ba = np.linalg.norm(ba) 
    #Distancia Estacion a Punto
    d_bc = np.linalg.norm(bc)
    #Distancia Epicentro a Estacion
    d_ac = np.linalg.norm((a-c))
    #----------#
    cosine_angle = np.dot(ba, bc) / (d_ba * d_bc)
    angle = np.arccos(cosine_angle)
    angle_d = np.degrees(angle)
    #---------------#
    DI = IE - IP
    LP = int(15)
    LS = int(15)
    if (angle_d>(180-LP) and angle_d<(180+LP)):
       # I_est = IE - (d_ba/ (d_ba+d_bc) )*DI
       d1 = np.linalg.norm(b - a)
       d2 = np.linalg.norm(c - a)
       cosine_angle2 = np.dot(d1, d2) / (d1 * d2)
       angle2 = np.arccos(cosine_angle2)
       angle_b = np.degrees(angle2)
       I_est = IE - (math.cos(angle_b)*d_ba/d_ac)*DI
    elif(angle_d<LS or angle_d > (360-LS)):
        d1 = np.linalg.norm(a - c)
        d2 = np.linalg.norm(b - c)
        cosine_angle3 = np.dot(d1, d2) / (d1 * d2)
        angle3 = np.arccos(cosine_angle3)
        angle_c = np.degrees(angle3)               
        angle_g = math.asin(math.sin(angle_c)*d1/d2)
        I_est = IE - DI*(d_bc*math.cos(angle_g))/(d_ac*math.cos(angle_c))
        
    else: I_est = 0
    return(I_est,angle_d)
    
    
def draw_map_background(m, ax):
    ax.set_facecolor('#729FCF')
    m.fillcontinents(color='#FAFAFA', ax=ax, zorder=0)
    m.drawcounties(ax=ax)
    m.drawstates(ax=ax)
    m.drawcountries(ax=ax)
    m.drawcoastlines(ax=ax)
KM = 150.
clat = 15.5
clon = -90.0
wid = 4500 * KM
hgt = 4000 * KM
m = Basemap(width=wid, height=hgt, rsphere=(6378137.00,6356752.3142),
            resolution='i', area_thresh=2500., projection='lcc',
            lat_1=13.0, lat_2=18.0, lat_0=clat, lon_0=clon)
fig = plt.figure()
ax = fig.add_subplot(111)
draw_map_background(m, ax)

#Leemos  el archivo
dfs = pd.read_csv('eventos/2019-02-01-1613.csv')

#-------------------------------------------#
C1 = []
C2 = []
C3 = []
#Este almacena todos los puntos 
for i in range(0,len(dfs)):
    C1.append(dfs['lon'][i])
    C2.append(dfs['lat'][i])
    C3.append(dfs['Intensidad'][i])
#Guardamos la intensidad en el epicentro
IO = C3[len(C3)-1]

#Listas de los puntos x,y e intensidad
PFx = []
PFy = []
PFI = []
#Ciclo para recorer el grid de Guate
for j in range(int(60000),int(320000),4000):
    for i in range(int(60000),int(540000),4000):
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
            
#Hacemos mapeo para obtener un rgb de la intensidad
#Pp = []
#for i in range(len(dfs)):
#    Pp.append(dfs['Intensidad'][i])

norm = mpl.colors.Normalize(-max(PFI), -min(PFI))
cmap = cm.hot
mc = cm.ScalarMappable(norm = norm, cmap = cmap)
VColor = []
for i in PFI:
    VColor.append(mcolors.to_hex(mc.to_rgba(-i)))
#print(VColor)

#Llenamos el mapa de estaciones
for i in range(len(PFx)):
    xpt,ypt = PFx[i],PFy[i]
    if(i!=len(dfs)):
       m.plot(xpt,ypt,marker='.',color=VColor[i])  # plot a dot there    
    else:
       m.plot(xpt,ypt,marker='o',color=VColor[i])  # plot a circle dot there 


# convert back to lat/lon. Pasamos de puntos x,y a long/lat
#lonpt, latpt = m(xpt,ypt,inverse=True)

       
plt.show()