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

fig, ax = plt.subplots(figsize=(12,8))
#Leemos la data de los sismos
dfs = pd.read_csv('Data/DataAV2.csv')
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
            lat_0=15.94, lon_0=-90.7943,
            llcrnrlon=x2, llcrnrlat=y2,urcrnrlon=x1, urcrnrlat=y1, epsg=4326)
    
    m.arcgisimage(service='Elevation/World_Hillshade', xpixels=900, dpi=100,verbose= True)                  
    #m.fillcontinents(lake_color='#46bcec')
    m.drawrivers(color='#46bcec')
    # m.drawmapboundary(zorder = 0)
    # m.drawcoastlines()
else:  
    m = Basemap(resolution='i', # c, l, i, h, f or None
            projection='tmerc', 
            lat_0=14.6569, lon_0=-90.51,
            llcrnrlon=-92.5, llcrnrlat=13.6,urcrnrlon=-88.0, urcrnrlat=18.0,epsg=4326)
    
    m.drawmapboundary(fill_color='#46bcec')       
    #Cuerpos de Agua
    m.drawrivers(color='#46bcec')           
    m.fillcontinents(color='#f2f2f2',lake_color='#46bcec')
    m.drawmapboundary(zorder = 0)
    m.drawcoastlines()
    m.arcgisimage(service='Elevation/World_Hillshade', xpixels=600, dpi=100,verbose= True)

# draw parallels and meridians.
parallels = np.arange(-92.,87.,0.5)
# Label the meridians and parallels
m.drawparallels(parallels,labels=[False,True,True,True])
# Draw Meridians and Labels
meridians = np.arange(-180.,181.,0.5)
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
            size=10
            marker='o'
        elif(ml>3.0):   
            color='y'
            size=8
            marker='o'
        else:           
            color = 'g'
            size=6
            marker='o'
        m.plot(xpt,ypt,marker=marker,color=color,markersize=size,markeredgecolor='k',markeredgewidth=1)  # plot a dot 


else:
    x2=x2-0.4
    x1 =x1+0.4
    y2 =y2-0.4
    y1 =y1+0.4
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
            
#Leemos nuestra shapefile
#Delimitaciones de Guatemala
m.readshapefile('Data/gtm/gtm_admbnda_adm0_ocha_conred_20190207', 'ej0',linewidth=1.5)
m.readshapefile('Data/gtm/gtm_admbnda_adm1_ocha_conred_20190207', 'ej1',drawbounds=True)
m.readshapefile('Data/fallas/fallas', 'fgt',drawbounds=True)

#Colocamos algunos municipios 
xc,yc = m(-90.4067400,15.4689600)
m.plot(xc,yc,marker ='*',color = 'k',markersize=20)
xt,yt = m(-90.4067400+0.015,15.4689600+0.035)
ax.text(xt,yt,'Coban', fontsize=10)

xc,yc = m(-91.315506,15.804456)
m.plot(xc,yc,marker ='*',color = 'k',markersize=20)
xt,yt = m(-91.315506+0.02,15.804456+0.03)
ax.text(xt,yt,'Santa Cruz Barillas', fontsize=10)

xc,yc = m(-91.034722,15.487222)
m.plot(xc,yc,marker ='*',color = 'k',markersize=20)
xt,yt = m(-91.034722+0.02,15.487222+0.03)
ax.text(xt,yt,'Chajul', fontsize=10)
#bbox=dict(boxstyle = "square",facecolor = "white")


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


# patches   = []
# for info, shape in zip(m.ca_info, m.ca):
#     patches.append( Polygon(np.array(shape), True) )      
# ax.add_collection(PatchCollection(patches, facecolor= '#85adad', edgecolor='w', linewidths=0.01, zorder=2))

if(Opc==False): m.readshapefile('Data/gtm/gtm_admbnda_adm2_ocha_conred_20190207', 'ej2',drawbounds=False)

#Titulo
plt.title("Sismicidad 2020-11-01 a 2020-12-10")
#Guardar Imagen
plt.savefig('Imagenes/Enjambre2020-11.png', bbox_inches='tight')
plt.show()
