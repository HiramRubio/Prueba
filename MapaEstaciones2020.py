# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 03:05:25 2021

@author: Steven Rubio
Mapa con las estaciones en la red nacional/metropolitana
"""

from openpyxl import load_workbook
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

#Nombres
CIUDAD = ['VILL','SJPIN','CCONS','CBIL','NRNJO','SMP','SPAYM','BVH','ALUX']

wb = load_workbook(filename = 'Data/CoordenadasAcelerómetros.xlsx', data_only =True)
#Guardamos todos los nombres de hojas
sheets = wb.sheetnames

#Mapa Ciudad
Ciudad = wb['ETNA2 INSTALADOS CIUDAD']
Nacional = wb['ETNA2 INSTALADOS DEP']
#Variables 
Names = []
Lat = []
Lon = []

if(True):
    #Ciclo 1
    for element in Ciudad.iter_rows(min_row=2,max_row = 40,min_col=2,max_col=6,values_only=True):
        if(element[0] != None):
            #print(element)
            Names.append(element[0])
            Lat.append(element[3])
            Lon.append(element[4])
    
    #Se obtienen coordenadas máximas
    x1,x2 = max(Lon),min(Lon)
    y1,y2 = max(Lat),min(Lat)
    y2=y2-0.3
    y1=y1+0.3
    x1=x1+0.25
    x2=x2-0.2
    
    #Inicio de plot
    fig, ax = plt.subplots(figsize=(8,8))
    
    m = Basemap(resolution='i', # c, l, i, h, f or None
            projection='tmerc', 
            lat_0=15.74, lon_0=-90.15,
            llcrnrlon=x2, llcrnrlat=y2,urcrnrlon=x1, urcrnrlat=y1, epsg=4326)
    
    #m.arcgisimage(service='Elevation/World_Hillshade', xpixels=900, dpi=100,verbose= True)                            
    m.fillcontinents(color='#f2f2f2',lake_color='#46bcec')
    #Leemos nuestra shapefile
    #Delimitaciones de Guatemala
    m.readshapefile('Data/gtm/gtm_admbnda_adm0_ocha_conred_20190207', 'ej0',linewidth=1.5)
    m.readshapefile('Data/gtm/gtm_admbnda_adm1_ocha_conred_20190207', 'ej1',drawbounds=True)
    
    #Se plotean las estacon
    for lat,lon,name in zip(Lat,Lon,Names):
        x,y = m(lon,lat)
        plot = ax.plot(x,y,'s',marker='^',color='r', markersize=10,markeredgecolor = 'k')
        #Plot del nombre de algunas estaciones
        if name in CIUDAD:
            ax.text(x+0.001,y+0.001,name,fontsize=8,color='r',rotation=45,bbox=dict(boxstyle = "square",
          facecolor = "white"))
            
if(False):
    #Ciclo 1
    for element in Nacional.iter_rows(min_row=2,max_row = 40,min_col=2,max_col=6,values_only=True):
        if(element[0] != None):
            #print(element)
            Names.append(element[0])
            Lat.append(element[3])
            Lon.append(element[4])
    
        #Se obtienen coordenadas máximas
    x1,x2 = max(Lon),min(Lon)
    y1,y2 = max(Lat),min(Lat)
    y2=y2-0.3
    y1=y1+2.5
    x1=x1+0.4
    x2=x2-0.2
    
    #Inicio de plot
    fig, ax = plt.subplots(figsize=(8,8))
    
    m = Basemap(resolution='i', # c, l, i, h, f or None
            projection='tmerc', 
            lat_0=15.74, lon_0=-90.15,
            llcrnrlon=x2, llcrnrlat=y2,urcrnrlon=x1, urcrnrlat=y1, epsg=4326)
    
    #m.arcgisimage(service='Elevation/World_Hillshade', xpixels=900, dpi=100,verbose= True)                            
    m.fillcontinents(color='#f2f2f2',lake_color='#46bcec')
    m.drawcoastlines(color='#0000ff')
    #Leemos nuestra shapefile
    #Delimitaciones de Guatemala
    m.readshapefile('Data/gtm/gtm_admbnda_adm0_ocha_conred_20190207', 'ej0',linewidth=1.5)
    m.readshapefile('Data/gtm/gtm_admbnda_adm1_ocha_conred_20190207', 'ej1',drawbounds=True)
    
    #Se plotean las estacon
    for lat,lon,name in zip(Lat,Lon,Names):
        x,y = m(lon,lat)
        plot = ax.plot(x,y,'s',marker='^',color='g', markersize=10,markeredgecolor = 'k')
        #Plot del nombre de algunas estaciones
        ax.text(x+0.01,y+0.01,name,fontsize=8,color='g',rotation=30,bbox=dict(boxstyle = "square",
          facecolor = "white"))