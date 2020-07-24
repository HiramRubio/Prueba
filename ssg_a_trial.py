# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 03:40:59 2020

@author: HRV
"""

import pandas as pd
from rich.console import Console
from folders_finder import *
from stations_extractor import *

homeDir = "C:/Users/HRV/Desktop/Post-U/Trabajo/Prueba/Data/Eventos/"
EventosD = ['2020-07-15-2054']
dfs = pd.read_csv('Data/Informe2A_Mex_Sup.csv')
name = EventosD[0]

events_station_extractor(EventosD,name,homeDir)


#Extraccion de información de un evento
def event_info_extractor(Evento,homeDir):
    # ----------
    # Entradas:
    # Evento    = Nombre del Folder
    # homeDir   = Directorio donde se encuentran los eventos
    # ----------
    # Salidas:
    # dataF     = Lat, lon, prof, tiempo, magnitud
    # ----------      
    name    = Evento
    year    = name[0:4]
    month   = name[5:7]
    day     = name[8:10]
    hour    = name[11:16]
    
    #Definimos el directorio madre y abrimos el evento
    #homeDir = "C:/Users/HRV/Desktop/Post-U/Trabajo/Prueba/Data/Eventos/"
    path = homeDir+str(year)+'/'+str(month)+'/'+str(name)
    E = False
    
    #Progra defensiva para no ingresar un evento que no se encuentra en el path
    try:
        dirs = os.listdir( path )
        E = True
    
    except FileNotFoundError:
        console.print("Evento "+str(name)+" no existe",style="bold red")
        console.print('Path:'+path+'/')
        return 0
       
    if(E):
        
        #Obtenemos el día del año del evento
        path2 = path+'/'+str(year)
                    
        #Progra defensiva para no ingresar un evento que no se encuentra en el path
        try:
            dirs2 = os.listdir( path2 )
            E = True
        
        except FileNotFoundError:
            console.print("Evento "+str(name)+" no tiene la carpeta año",style="bold red")      
            return 0
    
        nday = dirs2[0]
        #Corrección para evitar archivo DS_Store
        if(len(nday)>3):    nday = dirs2[1]
        #Construimos el nombre del evento>
        if(len(dirs2)>1 and len(dirs2[1])==3):
            nday = dirs2[1]
        eventN = path+'/'+year+nday+hour
        text = []
        with open(eventN+".origin", 'r') as f:
            for i in f:
                if (i[0:4]!='-999'):
                    text.append(str(i[2:]))
                                
        #Cortamos los espacios en blanco para obtener solo la data
        data  = text[0].split("  ",36)
        data2 = text[0]
        mg = data2[163:167]
        #Solo guardamos los primeros 5 datos: Lat, lon, prof, tiempo, magnitud
        #El tiempo se encuentra en un formato conocido como Unix Epoch
        Opcion = 0
        if(data2[17:21] == '    ' and Opcion == 0): 
            #print('Evento 1 digito')
            Opcion = 1
        if(data2[17:20] == '   ' and Opcion == 0): 
            #print('Evento 2 digitos')
            Opcion = 2
        if(data2[17:19] == '  ' and Opcion == 0): 
            #print('Evento 3 digitos')
            Opcion = 3
        
        #Eventos de profundidad con 2 digitos
        if(Opcion == 2): 
            dataF = (data[0],data[1],data[2],data[3],mg)
        #Eventos de profundidad con 1 digito
        if(Opcion == 1):  
            dataF = (data[0],data[1],data[3],data[4],mg)
        if(Opcion == 3):  
            dataF = (data[0],data[1],data[2],data[3],mg)

            
        #Revisamos los valores de magnitud y profundidad
        if(dataF[2]==''):    
            console.print("Evento "+str(name)+" con error en profundidad (.origin)",style="bold red") 
        if(dataF[4]=='-1' or dataF[4]=='' ):    
            console.print("Evento "+str(name)+" con error en magnitud (.origin)",style="bold red") 
           
    return dataF


def event_plot_stations(name,homeDir):
        # ----------
        # Entradas:
        # name      = Nombre del folder
        # homeDir   = Directorio donde se encuentran los eventos
        # ----------
        # Salidas:
        # Plot con estaciones y evento
        # ----------
        
    #Leemos el archivo con las estaciones del evento
    dfe = pd.read_csv(homeDir+str(name)+'_estaciones.csv')
    
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
    
    #Leemos Latitud, Longitud y Nombre de las estaciones
    e_lats = dfe['Lat']
    e_lons = dfe['Lon']
    e_names = dfe['Est']
    ploted = []
    
    #Generación de Plot
    for lat,lon,name_E in zip(e_lats,e_lons,e_names):
        #Mapeo
        x,y = m(lon,lat)
        #Si la estación ya se ploteo, se omite
        if(name_E in ploted):
            pass
        else:    
            #Punto y texto
            plt.plot(x,y,marker='*',color='r')
            ax.text((x+10),(y+10),name_E, fontsize=6)
            #Se agrega a la lista de Estaciones Ploteadas
            ploted.append( name_E ) 
    
    #Extraemos la informacion del evento
    e_main = event_info_extractor(name,homeDir)
    #Lat y Lon del Epicentro
    xp = float(e_main[0])
    yp = float(e_main[1])
    x,y = m(yp,xp)
    plt.plot(x,y,marker='^',color='b')
    
    Mensaje = 'Evento: '+str(name)+', Mag: '+str(e_main[4])+', Prof:'+str(e_main[2])
    plt.title(Mensaje)
    plt.show()    
        
    return True




event_plot_stations(name,homeDir)