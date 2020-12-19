# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 18:39:22 2020

@author: HRV
Mapa de los eventos sismicos más importantes del primer semestre de 2020
Solicitado por Grace
"""

import os, sys, math
import pandas as pd
import numpy as np
        
dfe = pd.read_csv('Data/Informe3AG.csv')
#Importamos librerias
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

#Creamos grafica 
fig, ax = plt.subplots(figsize=(8,8))
#Mapa Nacional GT
m = Basemap(resolution='c', # c, l, i, h, f or None
    lat_0=14.6569, lon_0=-90.51,
    llcrnrlon=-96.30, llcrnrlat=12.50,urcrnrlon=-87.58, urcrnrlat=18.42,epsg=4326,
    projection='tmerc')
  
#Cargamos el "fondo# del mapa
m.arcgisimage(service='World_Terrain_Base', xpixels=1600, dpi=200,verbose= True)
#Leemos nuestra shapefile, no los activamos todos
m.readshapefile('Data/gtm/gtm_admbnda_adm0_ocha_conred_20190207', 'ej0',linewidth=1.5)
m.readshapefile('Data/gtm/gtm_admbnda_adm1_ocha_conred_20190207', 'ej1',drawbounds=True)
m.drawrivers(color='#0000ff')
#Leemos Latitud, Longitud y Nombre de las estaciones
e_lats = dfe['lat']
e_lons = dfe['lon']
e_names = dfe['ml']
#Colores Utilizados
colors = ['#C0392B','#943126','#A93226','#CD6155','#922B21','#641E16']
ploted = []
d = 0
n = 1

#Generación de Plot
for lat,lon,name_E,color in zip(e_lats,e_lons,e_names,colors):
    #Mapeo
    x,y = m(lon,lat)
    #Si la estación ya se ploteo, se omite
    if(name_E in ploted):
        pass
    else:    
        #Punto y texto
        plt.plot(x,y,marker='*',color=color,markersize=8)
        xp,yp = m(-96.0,14.0-d)
        ax.text((xp),(yp),str(n)+'.', fontsize=12)
        plt.plot(xp+0.30,yp+0.07,marker='*',color=color,markersize=7)
        #Se agrega a la lista de Estaciones Ploteadas
        ploted.append( name_E ) 
        d = d +0.25
        n = n+1

# draw parallels and meridians.
parallels = np.arange(-96.,87.,1.0)
# Label the meridians and parallels
m.drawparallels(parallels,labels=[False,True,True,True])
# Draw Meridians and Labels
meridians = np.arange(-180.,181.,1)
m.drawmeridians(meridians,labels=[True,True,False,True])

#Título
Mensaje = 'Eventos destacados del primer semestre 2020'
plt.title(Mensaje)
plt.show()    