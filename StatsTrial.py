# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 03:09:02 2020

@author: HRV
"""


# importing Statistics module 
from statistics import mean, stdev, StatisticsError

import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np
from folders_finder import *
from stations_extractor import * 

#homeDir = '/antelope/analysis/eventos/'
homeDir = "C:/Users/HRV/Desktop/Post-U/Trabajo/Prueba/Data/Eventos/"

dfs = pd.read_csv("C:/Users/HRV/Desktop/Post-U/Trabajo/Prueba/Data/Eventos/bugFree_estaciones.csv")
#dfs = pd.read_csv("/antelope/analysis/eventos/Todos_Prof_estaciones.csv")

#Copia
df2 = dfs.copy()

#Cantidad de eventos registrados
fldrs = df2['Folder']
n_fldrs = len(np.unique(fldrs))
#Filtrado por estación 
Ests = df2['Est']
names = np.unique(Ests)


LB = ['Prof', 'mag','Dist (km) ']
dataF = []
#Recorremos todas las estaciones
for NAME in names:
    dataE = []
    print('Estacion: '+str(NAME))
    #Nombre de la estación 
    dataE.append(NAME)
    df3 = df2[df2['Est'].isin([NAME])]
    #Filtrado por onda P
    df2P = df3[df3['Onda'].isin(['P'])]
    
    #Lat 
    x = df2P['Lat']
    x2 = np.unique(x)
    dataE.append(x2[0])
    #Lon
    x = df2P['Lon']
    x2 = np.unique(x)
    dataE.append(x2[0])
    
    #Recorremos todas las variables
    for col in LB:
        var = df2P[col]
        var_m = mean(var) 
        
        dataE.append(var_m)
        #Intentamos obtener la desviacion estandat
        try:
            var_d = stdev(var)
        #Manejo de error por falta de datos
        except StatisticsError:
            var_d = 0
            
        dataE.append(var_d)    
    #Numero de eventos detectados
    n = len(df2P)
    dataE.append(n)
    dataE.append(float(n/n_fldrs))       
    
    dataF.append(dataE)
    # #plt.hist(profs, density=True)  # `density=False` would make counts
    # plt.errorbar(m,i,xerr=stdeve/2, fmt='o')
    # plt.xlabel('Magnitud')

    # #plt.title('Estación: '+names[i]+'. Var ='+str(LB[2])+', Media: '+str(np.round(m,3))+', dvs: '+str(np.round(stdeve,3)))
    # plt.title('Media y desviacionS de cada estación')
    # print("Mean of sample is % s " 
    #      % (m)) 
    # print("Standard Deviation of sample is % s " 
    #     % (stdeve) )
        
    
    if(False):
            #Importamos librerias
        from mpl_toolkits.basemap import Basemap
        import matplotlib.pyplot as plt
        #Creamos grafica 
        fig, ax = plt.subplots(figsize=(8,8))
        #Mapa Nacional GT
        m = Basemap(resolution='l', # c, l, i, h, f or None
            lat_0=14.6569, lon_0=-90.51,
            llcrnrlon=-92.93, llcrnrlat=13.15,urcrnrlon=-87.58, urcrnrlat=18.42,
            projection='tmerc')
        #Colores    
        m.drawmapboundary(fill_color='#46bcec')                  
        m.fillcontinents(color='#f2f2f2',lake_color='#46bcec')
        #Leemos nuestra shapefile, no los activamos todos
        m.readshapefile('Data/gtm/gtm_admbnda_adm0_ocha_conred_20190207', 'ej0',linewidth=1.5)
        m.readshapefile('Data/gtm/gtm_admbnda_adm1_ocha_conred_20190207', 'ej1',drawbounds=True)
        
        #Leemos Latitud, Longitud de la estacion para plotear
        lat = df2P['Lat']
        lon = df2P['Lon']
        lonc = np.unique(lon)
        latc = np.unique(lat)
        x,y = m(lonc[0],latc[0])
        plt.plot(x,y,marker='^',color='r')
        
        #Nombre de todos los folders
        fdrs = df2P['Folder']
        #Evitamos que aparezca uno repetido
        listf = np.unique(fdrs)
        
        #Generación de Plot
        for event in listf:
            #Extraemos la informacion del evento
            e_main = event_info_extractor(event,homeDir)
            #Lat y Lon del Epicentro
            xp = float(e_main[0])
            yp = float(e_main[1])
            x,y = m(yp,xp)
            plt.plot(x,y,marker='*',color='b')
        
        #Mensaje = 'Evento: '+str(name)+', Mag: '+str(e_main[4])+', Prof:'+str(e_main[2])
        #plt.title(Mensaje)
#plt.ylabel('Probability')    
#plt.title('Estación: '+names[i]+'. Var ='+str(LB[2])+', Media: '+str(np.round(m,3))+', dvs: '+str(np.round(stdeve,3)))
#plt.title('Media y desviacionS de cada estación, Prof')
#plt.show()  

dfs_n = pd.DataFrame(dataF,columns=['Est','Lat','Lon','prof_m','prof_d','mag_m','mag_d','dist_m','dist_d','eventos','kd'])
dfs_n.to_csv(homeDir+'/'+'Resumen_estaciones_P.csv',index=True)               