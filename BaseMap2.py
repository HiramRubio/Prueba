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
#from matplotlib.colors import Normalize
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.colors as mcolors
import  matplotlib.cm as cm

fig, ax = plt.subplots(figsize=(8,8))
#m = Basemap(resolution='i', # c, l, i, h, f or None
#           lat_0=14.6569, lon_0=-90.51,
#            llcrnrlon=-92.93, llcrnrlat=13.15,urcrnrlon=-87.58, urcrnrlat=18.42, epsg=4326)

m = Basemap(resolution='i', # c, l, i, h, f or None
        lat_0=14.6569, lon_0=-90.51,
        llcrnrlon=-92.82, llcrnrlat=11.80,urcrnrlon=-86.10, urcrnrlat=19.00,
         projection='merc')

# http://server.arcgisonline.com/arcgis/rest/services
#   World_Physical_Map
#   World_Shaded_Relief
#   World_Street_Map
#   World_Topo_Map
#   World_Terrain_Base

#m.arcgisimage(service='World_Physical_Map', xpixels = 2500, verbose= True)
m.drawmapboundary(fill_color='#46bcec')                  
m.fillcontinents(color='#f2f2f2',lake_color='#46bcec')
m.drawcoastlines()
m.drawmapscale(-91.7, 12.2, -90.51, 14.6569, 150 , barstyle='fancy')
# draw parallels and meridians.
parallels = np.arange(-92.,87.,1.)
# Label the meridians and parallels
m.drawparallels(parallels,labels=[False,True,True,True])
# Draw Meridians and Labels
meridians = np.arange(-180.,181.,1.)
m.drawmeridians(meridians,labels=[True,True,False,True])
      
#Leemos nuestra shapefile, no los activamos todos
m.readshapefile('Data/gtm/gtm_admbnda_adm0_ocha_conred_20190207', 'ej0',linewidth=1.0)
m.readshapefile('Data/gtm/gtm_admbnda_adm1_ocha_conred_20190207', 'ej1',drawbounds=False)
m.readshapefile('Data/gtm/gtm_admbnda_adm2_ocha_conred_20190207', 'ej2',drawbounds=False)
m.readshapefile('Data/ale/ZONASSISMOMOD', 'ej3',drawbounds=True)
#print(m.ej3_info)

#Resaltamos un area en especifico
for info, shape in zip(m.ej3_info, m.ej3):
    #Delimitar todas las zonas
    for a in info['ZONA']:
        x, y = zip(*shape) 
        m.plot(x, y, marker=None,color='k')
    #Delimitar una zona es especifico
#    if info['ZONA'] == 'G3':
#        x, y = zip(*shape) 
#        m.plot(x, y, marker=None,color='k')
        
patches   = []
#Pintamos un area en especifico
for info, shape in zip(m.ej3_info, m.ej3):
    #Pintar todas las zonas
    #for a in info['ZONA']:
    #    patches.append( Polygon(np.array(shape), True))
    #Pintar una zona en especifico
    if info['ZONA'] == 'G3':
        patches.append( Polygon(np.array(shape), True))

colors = ['b']        
#colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']      
ax.add_collection(PatchCollection(patches, facecolor= colors, edgecolor='k', linewidths=1., zorder=2, alpha=0.3))
plt.title("Mapas Zonas Sismogenicas de Guatemala")
plt.show()