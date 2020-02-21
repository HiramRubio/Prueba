#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 05:42:03 2020

@author: rt
"""

# the representation of a point will be a tuple (x,y)
# the representation of a polygon wil be a list of points [(x1,y1), (x2,y2), (x3,y3), ... ]

# it is assumed that polygon is regular i.e. lines don't intersect each other (otherwise, it is questionable whether it is a polygon)

import sys
import copy
import time
import random

from pointInside import *

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.patches import PathPatch
import numpy as np
import pandas as pd
#-------------------------------------------------
#Solo creamos plots que luego vamos a llenar 
fig     = plt.figure()
ax      = fig.add_subplot(111)
#Creamos nuestro mapa, entre los argumentos se encuentran: La calidad, proyeccion
#Resolucion, centro y limites
map = Basemap(resolution='i', # c, l, i, h, f or None
            projection='merc', 
            lat_0=14.6569, lon_0=-90.51,
            llcrnrlon=-92.93, llcrnrlat=13.15,urcrnrlon=-87.58, urcrnrlat=18.42)

#Dibujamos el background de nuestro mapa
map.drawmapboundary(fill_color='#46bcec')
map.fillcontinents(color='#f2f2f2',lake_color='#46bcec')
map.drawcoastlines()

#Leemos las Shapefiles. Estas las consegui en un rincon oscuro de internet, 
#podemos generar las nuestras para pintar regiones, etc.
map.readshapefile('Data/gtm/gtm_admbnda_adm0_ocha_conred_20190207', 'ej0',linewidth=1.0)
map.readshapefile('Data/gtm/gtm_admbnda_adm1_ocha_conred_20190207', 'ej1',drawbounds=False)
map.readshapefile('Data/gtm/gtm_admbnda_adm2_ocha_conred_20190207', 'ej2',drawbounds=False)

patches   = []
patches2 = []
#Pintamos solamente la capital
for info, shape in zip(map.ej1_info, map.ej1):
    if info['ADM1_REF'] == 'Guatemala':
        patches.append( Polygon(np.array(shape), True))
        patches2.append(np.array(shape))
        #patches2.append(*shape)
#ax.add_collection(PatchCollection(patches, facecolor= 'm', edgecolor='k', linewidths=1., zorder=2))

for info, shape in zip(map.ej1_info, map.ej1):
    if info['ADM1_REF'] == 'Guatemala':
        x, y = zip(*shape) 
        #map.plot(x, y, marker=None,color='k')
ax.plot(x, y)    
#print(x)    
#Para ver la info del archivo shapefile
#print(map.ej2_info)
#plt.show()
#--------------------------------------------------------------
patches3 = []
for i in range(len(x)):
    patches3.append((x[i],y[i]))
    
poly = Polygon(patches3)
#print("Algo raro:" ,patches2[0][0][0],patches2[0][0][1])
#patches2 = map(patches2[])


#-------------------------------------------------------------------------------
dfs = pd.read_csv('Data/estaciones.csv')
#Creamos los colores para cada estacion
 
for i in range(len(dfs)):
    xpt,ypt = map(dfs['lon'][i],dfs['lat'][i])
    testP = (xpt,ypt)
    ax.plot(xpt,ypt, 'or')
    print("La estacion", dfs['Name'][i], "Esta dentro de la region: ",is_inside_sm(patches3,testP))
   # print(is_inside_postgis(test_polygon2, testP))
    #print(isPointInPath(testP,test_polygon2))
    #print(cn_PnPoly(testP,test_polygon2))



plt.show()

# -------------------------------------------------------------------------------
