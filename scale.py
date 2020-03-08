#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  8 06:21:30 2020

@author: rt
"""

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt


#map = Basemap(llcrnrlon=-10.5,llcrnrlat=35,urcrnrlon=4.,urcrnrlat=44.,
#             resolution='i', projection='tmerc', lat_0 = 39.5, lon_0 = -3.25)


map = Basemap(llcrnrlon=-92.93,llcrnrlat=13.15, urcrnrlon=-87.58, urcrnrlat=18.42,
             resolution='i', projection='tmerc',lat_0 = 14.6569, lon_0 = -90.51)

map.drawmapboundary(fill_color='aqua')
map.fillcontinents(color='#cc9955',lake_color='aqua')
map.drawcoastlines()

#map.drawmapscale(-7., 35.8, -3.25, 39.5, 500, barstyle='fancy')

map.drawmapscale(-92.3, 14.0, -90.51, 14.6569, 500, barstyle='fancy')

plt.show()


   # m = Basemap(resolution='i', # c, l, i, h, f or None
    #    lat_0=14.6569, lon_0=-90.51,
     #   llcrnrlon=-92.93, llcrnrlat=13.15,urcrnrlon=-87.58, urcrnrlat=18.42, epsg=4326,
      #   projection='tmerc')