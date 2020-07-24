# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 03:09:02 2020

@author: HRV
"""


# importing Statistics module 
import statistics 
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np
from folders_finder import *
from stations_extractor import * 

homeDir = '/antelope/analysis/eventos/'
# # creating a simple data - set 
# sample = [1, 2, 3, 4, 5, 3, 3, 2] 

# # calculating the mean of sample set 
# m = statistics.mean(sample)   
# # Prints standard deviation 
# # xbar is set to default value of 1 
# print("Mean of sample is % s " 
#                 % (m)) 

# print("Standard Deviation of sample is % s " 
#                 % (statistics.stdev(sample,xbar = m))) 



# plt.hist(sample, density=True)  # `density=False` would make counts
# plt.ylabel('Probability')
# plt.xlabel('Data');


dfs = pd.read_csv("C:/Users/HRV/Desktop/Post-U/Trabajo/Prueba/Data/Eventos/Todos_mg_01_605_estaciones.csv")
#dfs = pd.read_csv("/antelope/analysis/eventos/Todos_mg_01_605_estaciones.csv")

#Copia
df2 = dfs.copy()
#Filtrado por estación 
Ests = df2['Est']
names = np.unique(Ests)
for i in range(len(names)):
    if i == 1:
        print('Estacion: '+str(names[i]))
        df2 = df2[df2['Est'].isin([names[i]])]
        #Filtrado por onda
        df2P = df2[df2['Onda'].isin(['P'])]
        
        profs = df2P['Angle']
        plt.hist(profs, density=True)  # `density=False` would make counts
        plt.ylabel('Probability')
        plt.xlabel('Angulo (Grados) ');
        m = statistics.mean(profs)   
        stdeve = statistics.stdev(profs,xbar = m)
        plt.title('Estación: '+names[i]+'. Var = Angle, Media: '+str(np.round(m,3))+', dvs: '+str(np.round(stdeve,3)))
        
        #Importamos librerias
        from mpl_toolkits.basemap import Basemap
        import matplotlib.pyplot as plt
        
        if(False):
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
            plt.show()  
        print("Mean of sample is % s " 
                % (m)) 
        
        print("Standard Deviation of sample is % s " 
                        % (statistics.stdev(profs,xbar = m))) 
        