# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 04:40:10 2020

@author: Steven Rubio

Extraccion de informacion de estaciones. 
"""
import os, sys, math
import geopy.distance
import pandas as pd
from rich.console import Console
from rich.progress import track
console = Console()

def calculate_initial_compass_bearing(pointA, pointB):
    #Public Domain Code. Edit by Steven Rubio
    #Source :https://gist.github.com/jeromer/2005586
    if (type(pointA) != tuple) or (type(pointB) != tuple):
        raise TypeError("Only tuples are supported as arguments")

    lat1 = math.radians(pointA[0])
    lat2 = math.radians(pointB[0])

    diffLong = math.radians(pointB[1] - pointA[1])

    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
            * math.cos(lat2) * math.cos(diffLong))

    initial_bearing = math.atan2(x, y)
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360
    # Function to assign a degree to a compass point
    return compass_bearing

#Extraccion de información de estaciones de un evento
def event_stations_info_extractor(Evento,n_dat,homeDir):
    # ----------
    # Entradas:
    # Evento    = Nombre del Folder
    # n_dat     = Lista con la información de los instrumentos
    # homeDir   = Directorio donde se encuentran los eventos
    # ----------
    # Salidas:
    # dfs_n     = Data frame con información del evento
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
        console.print(" Evento "+str(name)+" no existe",style="bold red")
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
            console.print(" Evento "+str(name)+" no tiene la carpeta año",style="bold red")      
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
            console.print(" Evento "+str(name)+" con error en profundidad (.origin)",style="bold red") 
        if(dataF[4]=='-1' or dataF[4]=='' ):    
            console.print(" Evento "+str(name)+" con error en magnitud (.origin)",style="bold red") 
        if(mg == '9.00'):    
            console.print(" Evento "+str(name)+" con soluciones del sistema Automatico (.origin)",style="bold red")      
        
        text2 = []
        #Abrimos un evento
        try: 
            with open(eventN+".arrival", 'r') as f: 
                for i in f:
                    #Filtramos los datos que nos interesan de origin
                    a = str(i[0:75])
                    a = a.split()
                    #Quitamos la U y todos los arrivos 'del' o 'mL'
                    if(len(a)==8 and a[7]!='del' and a[7]!='ml'):
                        text2.append(a) 
                        
        except FileNotFoundError:
            console.print(" Evento "+str(name)+" no tiene .arrival",style="bold red")      
            return 0
        
        #Almacenamos la estacion y el tiempo que les tomo llegar a la onda en listas separadas  
        #Almacenamos todas las ondas P 
        ListP = []
        #print("Ondas P: ")
        for i in range(len(text2)):
            if(text2[i][7]=='P'):
                x = -float(dataF[3])+float(text2[i][1])
                ListP.append((text2[i][0],x))
        #        print((text2[i][0],x))
        
        #Almacenamos todas las ondas S
        ListS = []
        #print("Ondas S: ")
        for i in range(len(text2)):
            if(text2[i][7]=='S'):
                x = -float(dataF[3])+float(text2[i][1])
                ListS.append((text2[i][0],x))
        #        print((text2[i][0],x)) 
        
        #Creamos una lista con el nombre las estaciones con ondas P y S
        ListPS = []
        for i in range(len(ListP)):
            for j in range(len(ListS)):
                if(ListP[i][0]==ListS[j][0]): ListPS.append(ListP[i][0])
                
        #Extramos la Lat y Lon de las estaciones con ondas P y S registradas
        text3 = []
        Estx = []
        Esty = []
        with open(eventN+".site", 'r') as f:
            for i in f:
                #Filtramos los datos que nos interesan de origin
                a = str(i[0:45])
                a = a.split()
                #Quitamos la U y todos los arrivos 'del'
                if(a[2]=='-1' and a[0] in ListPS):
                    #Almacenamos: Nombre, Lat, lon, Dis (distancia al epicentro), angle
                    xEs,yEs = (float(a[4]),float(a[3]))
                    #Calculamos distancia euclidiana al epicentro
                    coords_1 = (yEs,xEs)
                    coords_2 = (float(data[0]),float(data[1]))
                    dist = geopy.distance.distance(coords_1, coords_2).km
                    #Calculamos el ángulo
                    angle = calculate_initial_compass_bearing(coords_2, coords_1)
                    #Adjuntamos todos los datos de ondas P
                    for i in range(len(ListP)):
                        if(ListP[i][0] == a[0]): time = ListP[i][1]   
                    text3.append((name,dataF[2],dataF[4],a[0],a[3],a[4],dist,angle,'P',time))
                    #Adjuntamos todos los datos de ondas S
                    for i in range(len(ListS)):
                        if(ListS[i][0] == a[0]): time = ListS[i][1]   
                    text3.append((name,dataF[2],dataF[4],a[0],a[3],a[4],dist,angle,'S',time))
                    #Almacenamos las coordenadas para ploteo
                    Estx.append(xEs)
                    Esty.append(yEs) 
        
        #Creamos un nuevo dataFrame con la informacion que necesitamos
        dfs_n = pd.DataFrame(text3,columns=['Folder','Prof','mag','Est','Lat','Lon','Dist (km) ','Angle','Onda','DeltaT (segundos)'])
        return dfs_n
    

def events_station_extractor(Eventos,name,homeDir):
    # ----------
    # Entradas:
    # Eventos   = Lista con nombres del Folders
    # name      = Nombre para el .csv
    # homeDir   = Directorio donde se encuentran los eventos
    # ----------
    # Salidas:
    # .csv      = Información de los eventos
    # ----------  
    
    n_dat = []
    #Recorremos la lista de eventos
    for i in track(range(len(Eventos))):
        #Unimos/concatenamos el data Frame anterior al nuevo
        if(i!=0):
            dataF = event_stations_info_extractor(Eventos[i],n_dat,homeDir)
            #Se evita concatenar eventos cuando existe un error en las carpetas o no existe
            if(type(dataF) != int and type(dataO) != int):   
                dataO = pd.concat([dataO,dataF]) 
        #Solo en el caso 1 no actualizamos el dataFrame
        else:
            dataO = event_stations_info_extractor(Eventos[i],n_dat,homeDir)
        
        i   #Track
    
    #Generamos un csv con todos los resultados.
    if(type(dataO) != int):     
        dataO.to_csv(homeDir+'/'+str(name)+'_estaciones.csv',index=True)
        console.print(' Evento Guardado',style="bold green")
    
  
     
#---------------------------*//------------------------------   

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
        console.print(" Evento "+str(name)+" no existe",style="bold red")
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
            console.print(" Evento "+str(name)+" no tiene la carpeta año",style="bold red")      
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
            console.print(" Evento "+str(name)+" con error en profundidad (.origin)",style="bold red") 
        if(dataF[4]=='-1' or dataF[4]=='' ):    
            console.print(" Evento "+str(name)+" con error en magnitud (.origin)",style="bold red") 
        if(mg == '9.00'):    
            console.print(" Evento "+str(name)+" con soluciones del sistema Automatico (.origin)",style="bold red") 
           
    return dataF

#---------------------------*//------------------------------  
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
