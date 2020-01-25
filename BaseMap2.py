#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 22:58:28 2020

@author: Steven
"""
#https://boundingbox.klokantech.com/
#westlimit=-92.93; southlimit=13.15; eastlimit=-87.58; northlimit=18.42

import matplotlib.pyplot as plt
import matplotlib.cm
 
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.colors import Normalize
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.colors as mcolors
import  matplotlib.cm as cm

fig, ax = plt.subplots(figsize=(8,8))
m = Basemap(resolution='i', # c, l, i, h, f or None
            projection='merc', 
            lat_0=14.6569, lon_0=-90.51,
            llcrnrlon=-92.93, llcrnrlat=13.15,urcrnrlon=-87.58, urcrnrlat=18.42)
 
m.drawmapboundary(fill_color='#46bcec')
m.fillcontinents(color='#f2f2f2',lake_color='#46bcec')

#Leemos la data de las estaciones
dfs = pd.read_csv('eventos/2019-12-19-1235.csv')
#Creamos los colores para cada estacion
Pp = []
for i in range(len(dfs)):
    Pp.append(dfs['Intensidad'][i])

norm = mpl.colors.Normalize(-max(Pp), -min(Pp))
cmap = cm.hot
mc = cm.ScalarMappable(norm = norm, cmap = cmap)
VColor = []

for i in Pp:
    VColor.append(mcolors.to_hex(mc.to_rgba(-i)))

#print(VColor)
for i in range(len(dfs)):
    xpt,ypt = m(dfs['lon'][i],dfs['lat'][i])
    m.plot(xpt,ypt,marker='.',color=VColor[i])  # plot a dot    
                 
#Leemos nuestra shapefile, no los activamos todos
m.readshapefile('Data/gtm/gtm_admbnda_adm0_ocha_conred_20190207', 'ej0',linewidth=1.0)
m.readshapefile('Data/gtm/gtm_admbnda_adm1_ocha_conred_20190207', 'ej1',drawbounds=True)
m.readshapefile('Data/gtm/gtm_admbnda_adm2_ocha_conred_20190207', 'ej2',drawbounds=False)

#Dibujamos solo la capital
#for info, shape in zip(m.ej1_info, m.ej1):
#    if info['ADM1_REF'] == 'Guatemala':
#        x, y = zip(*shape) 
#        m.plot(x, y, marker=None,color='k')
        
plt.show()