#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 21:39:22 2020

@author: Steven
"""

from __future__ import (absolute_import, division, print_function)

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import pandas as pd
import matplotlib as mpl
import matplotlib.colors as mcolors
import  matplotlib.cm as cm

def draw_map_background(m, ax):
    ax.set_facecolor('#729FCF')
    m.fillcontinents(color='#FAFAFA', ax=ax, zorder=0)
    m.drawcounties(ax=ax)
    m.drawstates(ax=ax)
    m.drawcountries(ax=ax)
    m.drawcoastlines(ax=ax)
KM = 150.
clat = 14.5
clon = -90.5
wid = 500 * KM
hgt = 700 * KM
m = Basemap(width=wid, height=hgt, rsphere=(6378137.00,6356752.3142),
            resolution='i', area_thresh=2500., projection='lcc',
            lat_1=14.20, lat_2=14.8, lat_0=clat, lon_0=clon)
fig = plt.figure()
ax = fig.add_subplot(111)
draw_map_background(m, ax)

#Leemos  el archivo
dfs = pd.read_csv('eventos/t2.csv')

Pp = []
for i in range(len(dfs)):
    Pp.append(dfs['amp'][i])

norm = mpl.colors.Normalize(-max(Pp), -min(Pp))
cmap = cm.hot
mc = cm.ScalarMappable(norm = norm, cmap = cmap)
VColor = []

for i in Pp:
    VColor.append(mcolors.to_hex(mc.to_rgba(-i)))

#print(VColor)

for i in range(len(dfs)):
    xpt,ypt = m(dfs['lon'][i],dfs['Lat'][i])
    #if(i!=len(dfs)-1):
    m.plot(xpt,ypt,marker='.',color=VColor[i])  # plot a blue dot there    
    #else:
    #   m.plot(xpt,ypt,marker='o',color=VColor[i])  # plot a red dot there 

plt.show()