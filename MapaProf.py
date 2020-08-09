# -*- coding: utf-8 -*-
"""
Created on Fri May 29 05:38:06 2020

@author: HRV
Mapa regiones de profundidad utilizando SF proporcionadas por Alejandra
"""

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
#from matplotlib.patches import PathPatch
import numpy as np

fig, ax = plt.subplots(figsize=(8,8))
#Nacional
m = Basemap(resolution='i', # c, l, i, h, f or None
    lat_0=14.6569, lon_0=-90.51,
    llcrnrlon=-92.93, llcrnrlat=13.15,urcrnrlon=-87.58, urcrnrlat=18.42,
    projection='tmerc')
    
m.drawmapboundary(fill_color='#46bcec')                  
m.fillcontinents(color='#f2f2f2',lake_color='#46bcec')
#Leemos nuestra shapefile, no los activamos todos
m.readshapefile('Data/gtm/gtm_admbnda_adm0_ocha_conred_20190207', 'ej0',linewidth=1.5)
m.readshapefile('Data/gtm/gtm_admbnda_adm1_ocha_conred_20190207', 'ej1',drawbounds=True)
m.readshapefile('Data/prof2/PDN','pd',drawbounds=False)
m.readshapefile('Data/prof2/PPN','pp',drawbounds=False)
m.readshapefile('Data/prof2/PIN','pi',drawbounds=False)
m.readshapefile('Data/prof2/PSN','ps',drawbounds=False)

# patches   = []
# #Pintamos la region 1
# Mensaje = 'Región Difusa'
# for info, shape in zip(m.pd_info, m.pd):
#     patches.append( Polygon(np.array(shape), True) )
# ax.add_collection(PatchCollection(patches, facecolor= 'b', edgecolor='k', linewidths=1., zorder=2,alpha=0.2))

patches   = []
#Pintamos la region 2
Mensaje = 'Región Profunda'
for info, shape in zip(m.pp_info, m.pp):
    patches.append( Polygon(np.array(shape), True) )
ax.add_collection(PatchCollection(patches, facecolor= 'r', edgecolor='k', linewidths=1., zorder=2,alpha=0.2))

# patches   = []
# #Pintamos la region 3
# Mensaje = 'Región Intermedia'
# for info, shape in zip(m.pi_info, m.pi):
#     patches.append( Polygon(np.array(shape), True) )
# ax.add_collection(PatchCollection(patches, facecolor= 'g', edgecolor='k', linewidths=1., zorder=2,alpha=0.2))

# patches   = []
# # Pintamos la region Superficial
# Mensaje = 'Región Superficial'
# for info, shape in zip(m.ps_info, m.ps):
#     patches.append( Polygon(np.array(shape), True) )
# ax.add_collection(PatchCollection(patches, facecolor= 'y', edgecolor='k', linewidths=1., zorder=2,alpha=0.2))

#Titulo
plt.title(Mensaje)
plt.show()