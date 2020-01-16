#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 10:19:33 2019

@author: Grace
@edith: Steven
"""

import folium
import pandas as pd

#Coloco el nombre del excel y de la pagina que quiero abrir
#Ciudad
#Cambie el nombre del excel para que fuera mas facil. Podes cambiarlo
dfs1 = pd.read_excel('CoordAcce.xlsx', sheet_name='ETNA2 INSTALADOS CIUDAD',header=None)
#Departamentales
dfs2= pd.read_excel('CoordAcce.xlsx', sheet_name='ETNA2 INSTALADOS DEP',header=None)
#----------------------------#
#Nombre
Nombres_1 = dfs1[1].tolist()
Nombres_1 = Nombres_1[2:]
#Latitud
Latitud_1 = dfs1[4].tolist()
Latitud_1 = Latitud_1[2:] 
#Longitud
Longitud_1 = dfs1[5].tolist()
Longitud_1 = Longitud_1[2:]
#---------------------------------#
#Nombre
Nombres_2 = dfs2[1].tolist()
Nombres_2 = Nombres_2[2:]
#Latitud
Latitud_2 = dfs2[4].tolist()
Latitud_2 = Latitud_2[2:] 
#Longitud
Longitud_2 = dfs2[5].tolist()
Longitud_2 = Longitud_2[2:]

#Todos los que estan aca arriba son listas con la info, si las queres ver solo tenes que poner en consola print("Nombres_2"), por ejemplo. 
def dibujar_lineas_guia(mi_mapa):
    #LATITUDES
    linea1 = [[13.5,-95],[13.5,-87]]
    linea2 = [[14.5,-95],[14.5,-87]]
    linea3 = [[15,-95],[15,-87]]
    linea4 = [[16,-95],[16,-87]]
    linea5 = [[17,-95],[17,-87]]
    linea6 = [[18,-95],[18,-87]]
    linea7 = [[19,-95],[19,-87]]
    
    #LONGITUDES
    linea8 = [[13,-95],[19,-95]]
    linea9 = [[13,-94],[19,-94]]
    linea10 = [[13,-93],[19,-93]]
    linea11 = [[13,-92],[19,-92]]
    linea12 = [[13,-91],[19,-91]]
    linea13 = [[13,-90.5],[19,-90.5]]
    linea14 = [[13,-89],[19,-89]]
    linea15 = [[13,-88],[19,-88]]
    linea16 = [[13,-87],[19,-87]]
    
    #my_PolyLine1=folium.PolyLine(locations=linea1,weight=0.5,color="black" )
    my_PolyLine2=folium.PolyLine(locations=linea2,weight=0.5,color="black")
    #my_PolyLine3=folium.PolyLine(locations=linea3,weight=0.5,color="black")
    #my_PolyLine4=folium.PolyLine(locations=linea4,weight=0.5,color="black")
    #my_PolyLine5=folium.PolyLine(locations=linea5,weight=0.5,color="black")
    #my_PolyLine6=folium.PolyLine(locations=linea6,weight=0.5,color="black")
    #my_PolyLine7=folium.PolyLine(locations=linea7,weight=0.5,color="black")
    #my_PolyLine8=folium.PolyLine(locations=linea8,weight=0.5,color="black")
    #my_PolyLine9=folium.PolyLine(locations=linea9,weight=0.5,color="black")
    #my_PolyLine10=folium.PolyLine(locations=linea10,weight=0.5,color="black")
    #my_PolyLine11=folium.PolyLine(locations=linea11,weight=0.5,color="black")
    #my_PolyLine12=folium.PolyLine(locations=linea12,weight=0.5,color="black")
    my_PolyLine13=folium.PolyLine(locations=linea13,weight=0.5,color="black")
    #my_PolyLine14=folium.PolyLine(locations=linea14,weight=0.5,color="black")
    #my_PolyLine15=folium.PolyLine(locations=linea15,weight=0.5,color="black")
    #my_PolyLine16=folium.PolyLine(locations=linea16,weight=0.5,color="black")
    
    #mi_mapa.add_child(my_PolyLine1)
    mi_mapa.add_child(my_PolyLine2)
    #mi_mapa.add_child(my_PolyLine3)
    #mi_mapa.add_child(my_PolyLine4)
    #mi_mapa.add_child(my_PolyLine5)
    #mi_mapa.add_child(my_PolyLine6)
    #mi_mapa.add_child(my_PolyLine7)
    #mi_mapa.add_child(my_PolyLine8)
    #mi_mapa.add_child(my_PolyLine9)
    #mi_mapa.add_child(my_PolyLine10)
    #mi_mapa.add_child(my_PolyLine11)
    #mi_mapa.add_child(my_PolyLine12)
    mi_mapa.add_child(my_PolyLine13)
    #mi_mapa.add_child(my_PolyLine14)
    #mi_mapa.add_child(my_PolyLine15)
    #mi_mapa.add_child(my_PolyLine16)

#------------------------------------------------------------------------------#
m = folium.Map(
    location=[14.4837, -90.6165],
    zoom_start=8.0,
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}.png',
    attr = 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
)
#Opciones Para mapas
#tiles='https://stamen-tiles-{s}.a.ssl.fastly.net/toner-background/{z}/{x}/{y}{r}.png'
#'https://stamen-tiles-{s}.a.ssl.fastly.net/terrain/{z}/{x}/{y}{r}.{ext}'
#https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'
#https://leaflet-extras.github.io/leaflet-providers/preview/
tooltip = 'Estaciones'
 
for i in range(len(Nombres_1)):
    folium.RegularPolygonMarker([Latitud_1[i],Longitud_1[i]],radius=6,popup=Nombres_1[i], tooltip=Nombres_1[i], color= "black",fill_color="red").add_to(m)
    
#for i in range(len(Nombres_2)):
#   folium.RegularPolygonMarker([Latitud_2[i], Longitud_2[i]],radius=6,popup=Nombres_2[i], tooltip=Nombres_2[i], color= "black",fill_color='yellow').add_to(m)

dibujar_lineas_guia(m)
m.save("Estaciones_Cap2.html")
