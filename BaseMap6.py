#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 03:07:45 2020

@author: Steven
"""
#https://boundingbox.klokantech.com/
#westlimit=-92.93; southlimit=13.15; eastlimit=-87.58; northlimit=18.42

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import pandas as pd
import numpy as np

fig, ax = plt.subplots(figsize=(8,8))
Opc = True
#Nacional
if(Opc):
    m = Basemap(resolution='i', # c, l, i, h, f or None
        lat_0=14.6569, lon_0=-90.51,
        llcrnrlon=-92.93, llcrnrlat=13.15,urcrnrlon=-87.58, urcrnrlat=18.42, epsg=4326)
#Metropolitana
if(Opc==False):
    m = Basemap(resolution='i', # c, l, i, h, f or None
        lat_0=14.6569, lon_0=-90.51,
        llcrnrlon=-90.76, llcrnrlat=14.42,urcrnrlon=-90.384, urcrnrlat=14.71, epsg=4326)

# http://server.arcgisonline.com/arcgis/rest/services
#   World_Physical_Map
#   World_Shaded_Relief
#   World_Street_Map
#   World_Topo_Map
#   World_Terrain_Base

if(Opc==False):
    m.arcgisimage(service='World_Topo_Map', xpixels = 2500, verbose= True)
#m.arcgisimage(service='World_Terrain_Base', xpixels = 2500, verbose= True)
else:
    m.drawmapboundary(fill_color='#46bcec')                  
    m.fillcontinents(color='#f2f2f2',lake_color='#46bcec')

# draw parallels and meridians.
parallels = np.arange(-92.,87.,1.)
# Label the meridians and parallels
m.drawparallels(parallels,labels=[False,True,True,True])
# Draw Meridians and Labels
meridians = np.arange(-180.,181.,1.)
m.drawmeridians(meridians,labels=[True,True,False,True])

#Leemos la data de las estaciones
#Nacional
if(Opc):
    dfs = pd.read_csv('Data/Nacional.csv')
#Metropolitana
if(Opc==False):
    dfs = pd.read_csv('Data/Metropolitana.csv')

#Creamos los colores para cada estacion 
for i in range(len(dfs)):
    xpt,ypt = m(dfs['lon'][i],dfs['lat'][i])
    #Agregando un texto en el mapa
    if(dfs['Name'][i]=='SMARC'):
        ypt = ypt+0.1 
    #Ajuste Nacional
    if(Opc):h = 0.01
    #Ajuste Metropolitano
    else: h = 0.001
    #Size = 8 Nacional
    if(Opc): plt.text(xpt+h, ypt+h,dfs['Name'][i],bbox=dict(boxstyle="round",
                   ec=(1., 0.5, 0.5),
                   fc=(1., 0.8, 0.8),
                   ),size=7,rotation=30.)
    else: plt.text(xpt+h, ypt+h,dfs['Name'][i],size=6,rotation=30.)
    m.plot(xpt,ypt,marker='o',color='m')  # plot a dot   
                
#Leemos nuestra shapefile, no los activamos todos
m.readshapefile('Data/gtm/gtm_admbnda_adm0_ocha_conred_20190207', 'ej0',linewidth=1.5)
m.readshapefile('Data/gtm/gtm_admbnda_adm1_ocha_conred_20190207', 'ej1',drawbounds=True)
#Titulo
plt.title("Mapas Estaciones SSG")
#Guardar Imagen
#plt.savefig('Imagenes/EstacionesNacional.png', bbox_inches='tight')
plt.show()