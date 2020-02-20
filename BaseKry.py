#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 22:32:13 2020

@author: Steven
"""

import numpy as np
import pandas as pd
import glob
from pykrige.ok import OrdinaryKriging
from pykrige.kriging_tools import write_asc_grid
import pykrige.kriging_tools as kt
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Path, PathPatch
import matplotlib.colors as mcolors
import  matplotlib.cm as cm
import matplotlib as mpl
from geophysics import estacion
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection


#   Pruebas para hacer mascaras de regiones


# Leer un archivo
#---------------------**----------------------
#
#datafile='eventos/2019-07-31-0555.csv'
#df=pd.read_csv(datafile)
#lons=np.array(df['lon']) 
#lats=np.array(df['lat']) 
#data=np.array(df['int_i'])

#Leer el registro con Geophysics
#---------------------**----------------------
X0 = []
X1 = []
y = []
fac02 =  [('ACRIS', 1206.1448),('CAUST', 1182.828208), ('CDBOS',1179.0282), ('EXCEL', 1180.7432), ('ITC', 1184.6142), ('LSECB', 1190.994),  ('SJPIN',1180.5178),('CCONS',1178.7244)]
#fac02 = [('ACRIS', 3.686681571),('CAUST', 5.928297668), ('CDBOS',1.487064836), ('CSTER', 2.996806132), ('ITC', 3.461992973),('KINAL', 1.954327691), ('LSECB', 3.970137336), ('RGIL', 2.407856915), ('TADEO',1.840146918), ('SJPIN',4.68141169),('CCONS',1)]
for i in fac02:
    a = estacion(i[0])
    y.append(i[1])
    X0.append(a.longitud)
    X1.append(a.latitud)
#X = np.array(X)
#---------------------**----------------------
lons=np.array(X0) 
lats=np.array(X1) 
data=np.array(y)

#Creando un Grid con maximos/minimos o valores especificos
grid_space = 0.01
#llcrnrlon=-90.59, llcrnrlat=14.53,urcrnrlon=-90.346, urcrnrlat=14.73
#grid_lon = np.arange(np.amin(lons), np.amax(lons), grid_space) #grid_space is the desired delta/step of the output array 
grid_lon = np.arange(np.amin(lons)-1, np.amax(lons)+0.3, grid_space)
#grid_lon = np.arange(-90.59, -90.346, grid_space) #grid_space is the desired delta/step of the output array 
grid_lat = np.arange(np.amin(lats)-1, np.amax(lats)+0.3, grid_space)
#grid_lat = np.arange(14.53, 14.73, grid_space)

#Instancia Kriging Ordinario
OK = OrdinaryKriging(lons, lats, data, variogram_model='gaussian', verbose=True, enable_plotting=False,nlags=20)
z1, ss1 = OK.execute('grid', grid_lon, grid_lat)

xintrp, yintrp = np.meshgrid(grid_lon, grid_lat)
fig, ax = plt.subplots(figsize=(10,10))

#Creamos el baseMap en base a datos. Se puede ajustar esa resta.  
#m = Basemap(llcrnrlon=lons.min()-0.01,llcrnrlat=lats.min()-0.01,urcrnrlon=lons.max()+0.01,urcrnrlat=lats.max()+0.01, projection='merc', resolution='h',area_thresh=1000.,ax=ax,epsg=4326)
m = Basemap(resolution='i', # c, l, i, h, f or None
            lat_0=14.6569, lon_0=-90.51,
            llcrnrlon=-90.81, llcrnrlat=14.19,urcrnrlon=-90.09, urcrnrlat=14.97, epsg=4326)
#m = Basemap(resolution='i', # c, l, i, h, f or None
#            lat_0=14.6569, lon_0=-90.51,
#            llcrnrlon=-93.5, llcrnrlat=13.0,urcrnrlon=-87.58, urcrnrlat=18.52, epsg=4326)


#Dibujamos las costas y leemos Shape Files
m.drawcoastlines() #draw coastlines on the map
m.readshapefile('Data/gtm/gtm_admbnda_adm0_ocha_conred_20190207', 'ej0',linewidth=1.5)
m.readshapefile('Data/gtm/gtm_admbnda_adm1_ocha_conred_20190207', 'ej1',linewidth=1.5,drawbounds=False)
m.readshapefile('Data/gtm/gtm_admbnda_adm2_ocha_conred_20190207', 'ej2',linewidth=0.5,drawbounds=False)
#m.readshapefile('Qgis/Zonas', 'ej3',linewidth=2)
#print(m.ej2_info)
"""
patches   = []
#Pintamos solamente la capital
for info, shape in zip(m.ej1_info, m.ej1):
    if info['ADM1_REF'] == 'Guatemala':
        patches.append( Polygon(np.array(shape), True) )
        
ax.add_collection(PatchCollection(patches, facecolor= 'm', edgecolor='k', linewidths=1., zorder=2))
#"""  
#Colocamos solo la capital
#"""
for info, shape in zip(m.ej2_info, m.ej2):
    if info['ADM2_REF'] == 'Guatemala':
        x, y = zip(*shape) 
        m.plot(x, y, marker=None,color='k')
#"""   
x,y=m(xintrp, yintrp) # convert the coordinates into the map scales
ln,lt=m(lons,lats)

#Normalizamos la data para colorear
norm = mpl.colors.Normalize(vmin=min(data), vmax=max(data))
cmap1 = cm.jet
mc = cm.ScalarMappable(norm = norm, cmap = cmap1)
cs=ax.contourf(x, y, z1, np.linspace(min(data),max(data)+0.1,100),extend='both',cmap=cmap1, alpha = 1) #plot the data on the map.18
cbar=m.colorbar(cs,location='right',pad="7%") #plot the colorbar on the map

# draw parallels.
parallels = np.arange(-92.,87.,1.)
m.drawparallels(parallels,labels=[1,0,0,0],fontsize=14, linewidth=0.0) #Draw the latitude labels on the map
 
# draw meridians
meridians = np.arange(-180.,181.,1.)
m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=14, linewidth=0.0)

#"""
##getting the limits of the map:
x0,x1 = ax.get_xlim()
#x0,x1 = -90.81,-90.09
y0,y1 = ax.get_ylim()
#y0,y1 = 14.19,14.97
map_edges = np.array([[x0,y0],[x1,y0],[x1,y1],[x0,y1]])
##getting all polygons used to draw the coastlines of the map
polys = [p.boundary for p in m.landpolygons]
print("Polys 1:")
#print(polys)
##combining with map edges
#polys = [map_edges]+polys[:]
#print("Polys 2:")
#print(polys)

patches   = []
patches2   = []
patches3   = []
#Pintamos solamente la capital
for info, shape in zip(m.ej1_info, m.ej1):
    if info['ADM1_REF'] == 'Guatemala':
        patches.append(np.array(shape))
print("Patches: ")        
#print(patches)
#print(m.ej0_info)
for info, shape in zip(m.ej0_info, m.ej0):
    if info['ADM0_ES'] == 'Guatemala':
        patches2.append(np.array(shape))
print("Patches: ")        
#print(patches2)
for info, shape in zip(m.ej2_info, m.ej2):
    if info['ADM2_ES'] == 'Guatemala':
        patches3.append(np.array(shape))
print("Patches: ")        
#print(patches2)

polys = [map_edges]+patches3
##creating a PathPatch
codes = [
        [Path.MOVETO]+[Path.LINETO for p in p[1:]] 
        for p in polys
        ]
 
polys_lin = [v for p in polys for v in p]
 
codes_lin = [xx for cs in codes for xx in cs]
 
path = Path(polys_lin, codes_lin)
patch = PathPatch(path,facecolor='white', lw=0,alpha=1.0)

##masking the data outside the inland of taiwan
ax.add_patch(patch)
#"""
#Titulo
plt.title("Mapa de Espectro de aceleraciones en PGA")
#Guardar Imagen
#plt.savefig('Imagenes/EstacionesNacional.png', bbox_inches='tight')
plt.show()