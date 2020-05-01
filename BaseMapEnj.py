# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 21:17:33 2020

@author: Steven Rubio

Mapa de eventos: Utilizado para el análisis de enjambres


"""

#https://boundingbox.klokantech.com/
#westlimit=-92.93; southlimit=13.15; eastlimit=-87.58; northlimit=18.42

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import pandas as pd
import numpy as np
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

fig, ax = plt.subplots(figsize=(8,8))
#Leemos la data de los sismos
dfs = pd.read_csv('Data/Informe.csv')
Opc = False
x1,x2 = max(dfs['lon']),min(dfs['lon'])
y1,y2 = max(dfs['lat']),min(dfs['lat'])
y2=y2-0.03
y1=y1+0.03
x1=x1+0.02
x2=x2-0.02

#m.drawmapscale(-90.5, 14.31, -90.4, 14.4, 5 , barstyle='fancy')
# http://server.arcgisonline.com/arcgis/rest/services
#   World_Physical_Map
#   World_Shaded_Relief
#   World_Street_Map
#   World_Topo_Map
#   World_Terrain_Base
#   Elevation/World_Hillshade
#   Reference/World_Boundaries_and_Places_Alternate'

if(Opc==False):
    m = Basemap(resolution='i', # c, l, i, h, f or None
            projection='tmerc', 
            lat_0=14.6569, lon_0=-90.51,
            llcrnrlon=x2, llcrnrlat=y2,urcrnrlon=x1, urcrnrlat=y1, epsg=4326)
    
    m.arcgisimage(service='Elevation/World_Hillshade', xpixels=800, dpi=100,verbose= True)
    # m.drawmapboundary(fill_color='#46bcec')                  
    #m.fillcontinents(color='#f2f2f2',lake_color='#46bcec')
    # m.drawmapboundary(zorder = 0)
    # m.drawcoastlines()
else:  
    m = Basemap(resolution='i', # c, l, i, h, f or None
            projection='tmerc', 
            lat_0=14.6569, lon_0=-90.51,
            llcrnrlon=-92.5, llcrnrlat=13.6,urcrnrlon=-88.0, urcrnrlat=18.0,epsg=4326)
    
    m.drawmapboundary(fill_color='#46bcec')                  
    m.fillcontinents(color='#f2f2f2',lake_color='#46bcec')
    m.drawmapboundary(zorder = 0)
    m.drawcoastlines()
    #m.arcgisimage(service='Elevation/World_Hillshade', xpixels=600, dpi=100,verbose= True)

# draw parallels and meridians.
parallels = np.arange(-92.,87.,0.1)
# Label the meridians and parallels
m.drawparallels(parallels,labels=[False,True,True,True])
# Draw Meridians and Labels
meridians = np.arange(-180.,181.,0.1)
m.drawmeridians(meridians,labels=[True,True,False,True])

#Creamos los colores para cada estacion 
#xa = []
#ya = []
if(Opc==False):
    for i in range(len(dfs)):
        xpt,ypt = m(dfs['lon'][i],dfs['lat'][i])
        ml = dfs['ml'][i]
        if(ml>4.0):     
            color='r' 
            size=20
            marker='*'
        elif(ml>2.0):   
            color='y'
            size=8
            marker='o'
        else:           
            color = 'g'
            size=6
            marker='o'
        m.plot(xpt,ypt,marker=marker,color=color,markersize=size,markeredgecolor='k',markeredgewidth=1)  # plot a dot 

else:
    x2=x2-0.1
    x1 =x1+0.1
    y2 =y2-0.1
    y1 =y1+0.1
    xn = np.linspace(x2,x1, 100)
    yn = np.linspace(y2,y1, 100)
    xc1 = np.linspace(x1,x1, 100)
    xc2 = np.linspace(x2,x2, 100)
    yc1 = np.linspace(y1,y1, 100)
    yc2 = np.linspace(y2,y2, 100)
    m.plot(xn,yc1,marker=",",color="r")
    m.plot(xn,yc2,marker=",",color="r")
    m.plot(xc1,yn,marker=",",color="r")
    m.plot(xc2,yn,marker=",",color="r") 
    #Pintamos solamente la capital
            
#Leemos nuestra shapefile, no los activamos todos
m.readshapefile('Data/gtm/gtm_admbnda_adm0_ocha_conred_20190207', 'ej0',linewidth=1.5)
m.readshapefile('Data/gtm/gtm_admbnda_adm1_ocha_conred_20190207', 'ej1',drawbounds=False)

if(Opc==True):
    patches   = []
    for info, shape in zip(m.ej0_info, m.ej0):
        if info['ADM0_ES'] == 'Guatemala':
            patches.append( Polygon(np.array(shape), True) )      
    ax.add_collection(PatchCollection(patches, facecolor= '#85adad', edgecolor='k', linewidths=1., zorder=2))
    patches   = []
    for info, shape in zip(m.ej1_info, m.ej1):
        if info['ADM1_REF'] == 'Guatemala' or info['ADM1_REF'] == 'Santa Rosa' or info['ADM1_REF'] == 'Escuintla'  :
            patches.append( Polygon(np.array(shape), True) )      
    ax.add_collection(PatchCollection(patches, facecolor= '#527a7a', edgecolor='k', linewidths=1., zorder=2))

m.readshapefile('Data/gtm/gtm_admbnda_adm1_ocha_conred_20190207', 'ej1',drawbounds=False) 
m.readshapefile('Data/shp/gis_osm_water_a_free_1', 'ca',drawbounds=False)

patches   = []
for info, shape in zip(m.ca_info, m.ca):
    patches.append( Polygon(np.array(shape), True) )      
ax.add_collection(PatchCollection(patches, facecolor= '#85adad', edgecolor='w', linewidths=0.01, zorder=2))

if(Opc==False): m.readshapefile('Data/gtm/gtm_admbnda_adm2_ocha_conred_20190207', 'ej2',drawbounds=False)
#Titulo
plt.title("Enjambre Sismico 2020-04-19 > 2020-04-21")
#Guardar Imagen
plt.savefig('Imagenes/Enjambre202004B.png', bbox_inches='tight')
plt.show()
