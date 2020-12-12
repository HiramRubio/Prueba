#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 25 03:46:13 2020

@author: Steven
Mapa para pintar algun departamento en especifico

"""
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.patches import PathPatch
import numpy as np

#Solo creamos plots que luego vamos a llenar 
fig     = plt.figure()
ax      = fig.add_subplot(111)
#Creamos nuestro mapa, entre los argumentos se encuentran: La calidad, proyeccion
#Resolucion, centro y limites
map = Basemap(resolution='i', # c, l, i, h, f or None
            projection='merc', 
            lat_0=14.6569, lon_0=-90.51,
            llcrnrlon=-92.5, llcrnrlat=13.7,urcrnrlon=-88.0, urcrnrlat=17.9, epsg=4326)

#Dibujamos el background de nuestro mapa
map.drawmapboundary(fill_color='#46bcec')
map.fillcontinents(color='#f2f2f2',lake_color='#46bcec')
map.drawcoastlines()
#map.arcgisimage(service='Elevation/World_Hillshade', xpixels=1000, dpi=100,verbose= True) 

#Leemos las Shapefiles. Estas las consegui en un rincon oscuro de internet, 
#podemos generar las nuestras para pintar regiones, etc.
map.readshapefile('Data/gtm/gtm_admbnda_adm0_ocha_conred_20190207', 'ej0',linewidth=1.0)
map.readshapefile('Data/gtm/gtm_admbnda_adm1_ocha_conred_20190207', 'ej1',drawbounds=True)
map.readshapefile('Data/gtm/gtm_admbnda_adm2_ocha_conred_20190207', 'ej2',drawbounds=False)


# draw parallels and meridians.
parallels = np.arange(-92.,87.,1)
# Label the meridians and parallels
map.drawparallels(parallels,labels=[False,True,True,True])
# Draw Meridians and Labels
meridians = np.arange(-180.,181.,1)
map.drawmeridians(meridians,labels=[True,True,False,True])


x1,y1 = map(-91.5673,16.137500000000003)
x2,y2 = map(-89.7709,15.3042)
map.plot([x1, x2, x2, x1,x1],[y1,y1,y2,y2,y1],'r')


#Para colocar Parches de alguna shapefile

patches   = []
#Pintamos solamente la capital
for info, shape in zip(map.ej1_info, map.ej1):
    #if info['ADM1_REF'] == 'Alta Verapaz':
    patches.append( Polygon(np.array(shape), True) )
        
ax.add_collection(PatchCollection(patches, facecolor= '#8cd9b3', edgecolor='k', linewidths=1., zorder=2))

# #Colocamos solo los municipios de la capital
# for info, shape in zip(map.ej2_info, map.ej2):
#     if info['ADM1_ES'] == 'Alta Verapaz':
#         x, y = zip(*shape) 
#         map.plot(x, y, marker=None,color='k')
        

#Para ver la info del archivo shapefile
#print(map.ej2_info)
plt.savefig('Imagenes/ZonaEnjambre2020-11.png', bbox_inches='tight')
plt.show()
#-----------------------------------
