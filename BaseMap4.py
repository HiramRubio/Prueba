#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 22:51:02 2020

@author: Steven
"""
#https://boundingbox.klokantech.com/
#westlimit=-92.93; southlimit=13.15; eastlimit=-87.58; northlimit=18.42

import matplotlib.pyplot as plt
#import matplotlib.cm
 
from mpl_toolkits.basemap import Basemap
#from matplotlib.patches import Polygon
#from matplotlib.collections import PatchCollection
#from matplotlib.colors import Normalize
import pandas as pd
import numpy as np
#import matplotlib as mpl
#import matplotlib.colors as mcolors
#import  matplotlib.cm as cm
import math

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
            llcrnrlon=-92.93, llcrnrlat=13.15,urcrnrlon=-87.58, urcrnrlat=18.42, epsg=4326)
# http://server.arcgisonline.com/arcgis/rest/services
#   World_Physical_Map
#   World_Shaded_Relief
#   World_Street_Map
#   World_Topo_Map
#   World_Terrain_Base

m.arcgisimage(service='World_Physical_Map', xpixels = 2500, verbose= True)
#m.drawcoastlines(zorder = 0)
#m.drawcountries(zorder = 0)
#m.drawmapboundary(zorder = 0)
m.drawmapboundary(fill_color='#46bcec')                  
m.fillcontinents(color='#f2f2f2',lake_color='#46bcec')

#Leemos la data de las estaciones
dfs = pd.read_csv('eventos/2019-12-19-1235.csv')

#Guardamos los datos de cada estacion
VI = []
Lot = []
Lat = []
for i in range(len(dfs)):
    VI.append(dfs['Intensidad'][i])
    Lot.append(dfs['lon'][i])
    Lat.append(dfs['lat'][i])
#-----------------------------------#
n_est = len(Lot)-1      #Numero de estaciones sin el epicentro

ListI = []
Pts_x = []
Pts_y = []
for i in np.arange(-92.9,-87.5,0.05):
    for j in np.arange(13.2,18.3,0.05):
        #Recorremos todas las estaciones
        P = []
        for k in range(n_est-1):        
            xpt,ypt = m(Lot[k],Lat[k]) #Mapeo punto de la estacion
            #Estimacion de intensidad
            I_x,y = Intensidad_E(Lot[n_est],Lat[n_est],i,j,xpt,ypt,VI[n_est],VI[k])
            if(I_x != 0): P.append(I_x)
            #print(I_x)
        if(len(P)!=0):
            I_est = sum(w for w in P)/len(P)   
            ListI.append(I_est)
            Pts_x.append(i)
            Pts_y.append(j)
          
#Definimos nuestro mapeo
jet = plt.cm.get_cmap('viridis')
Pts_x.append(Lot[n_est])
Pts_y.append(Lat[n_est])
ListI.append(VI[n_est])
#print(ListI)

#Leemos nuestra shapefile, no los activamos todos
m.readshapefile('Data/gtm/gtm_admbnda_adm0_ocha_conred_20190207', 'ej0',linewidth=1.0)
m.readshapefile('Data/gtm/gtm_admbnda_adm1_ocha_conred_20190207', 'ej1',drawbounds=True)
m.readshapefile('Data/gtm/gtm_admbnda_adm2_ocha_conred_20190207', 'ej2',drawbounds=False)
#m.readshapefile('Data/ale/ZONASSISMOMOD', 'ej3',drawbounds=True)
#print(m.ej3_info)
sc = plt.scatter(Pts_x,Pts_y,c=ListI, vmin=min(ListI), vmax=max(ListI), cmap=jet, s=30, edgecolors='none',alpha = 0.4)           
#cbar = plt.colorbar(sc, shrink = 0.8)
#cbar.set_label("Intensidad")
plt.savefig('Imagenes/ImagenPrueba.png', bbox_inches='tight')
        