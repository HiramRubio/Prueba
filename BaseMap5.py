#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 21:11:06 2020

@author: STY
"""

#https://boundingbox.klokantech.com/
#westlimit=-92.93; southlimit=13.15; eastlimit=-87.58; northlimit=18.42

import matplotlib.pyplot as plt
#import matplotlib.cm
 
from mpl_toolkits.basemap import Basemap
import pandas as pd
import numpy as np
import math
import matplotlib as mpl
import matplotlib.colors as mcolors
import  matplotlib.cm as cm

#----------------------------------------------------------#
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
    LP = int(65)
    LS = int(65)
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
#----------------------------------------------------------#

fig, ax = plt.subplots(figsize=(8,8))
m = Basemap(resolution='i', # c, l, i, h, f or None
            lat_0=14.6569, lon_0=-90.51,
            llcrnrlon=-90.59, llcrnrlat=14.53,urcrnrlon=-90.346, urcrnrlat=14.73, epsg=4326)
# http://server.arcgisonline.com/arcgis/rest/services
#   World_Physical_Map
#   World_Shaded_Relief
#   World_Street_Map
#   World_Topo_Map
#   World_Terrain_Base
#m.arcgisimage(service='World_Physical_Map', xpixels = 2500, verbose= True)
m.drawcoastlines(zorder = 0)
m.drawmapboundary(zorder = 0)
m.drawmapboundary(fill_color='#46bcec')                  
m.fillcontinents(color='#f2f2f2',lake_color='#46bcec')

#Leemos la data de las estaciones
dfs = pd.read_csv('ddp/2019-04-16-0404_02.csv')
#Guardamos los datos de cada estacion
Pp = []
for i in range(len(dfs)):
    Pp.append(dfs['amp'][i])

norm = mpl.colors.Normalize(vmin=min(Pp), vmax=max(Pp))

cmap = cm.jet
mc = cm.ScalarMappable(norm = norm, cmap = cmap)
VColor = []

for i in Pp:
    VColor.append(mcolors.to_hex(mc.to_rgba(i)))
labels = str('Epicentro')
for i in range(len(dfs)):
    xpt,ypt = m(dfs['lon'][i],dfs['lat'][i])   
    m.plot(xpt,ypt,marker='.',color=VColor[i],alpha=0.027,markersize=24)  # plot a dot 
#-----------------------------------#
#Leemos nuestra shapefile
       
m.readshapefile('Qgis/Zonas', 'zonas',linewidth=2.0)
#Colocamos todos los puntos que calculamos anteriormente
#c = plt.scatter(Lot,Lat,c=VI, vmin=0.0, vmax=7.0, cmap=jet, s=40, edgecolors='none',alpha = 0.2)           
#cbar = plt.colorbar(sc, shrink = 0.8)   #Barra de color
#cbar.set_label("Amplificacion")
#plt.savefig('ddp_I/2019-04-16-0404_02.png', bbox_inches='tight')
plt.show()
#print(ListI)