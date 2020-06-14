# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 04:40:10 2020

@author: Steven Rubio
Abrir un evento y extraer si información solo con el nombre del evento

Prueba
"""
import os, sys, math
import geopy.distance
import pandas as pd


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


def event_stations_info_extractor(Evento,n_dat,homeDir):
          
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
        print("Evento "+str(name)+" no existe")      
        return 0
       
    if(E):
        
        #Obtenemos el día del año del evento
        path2 = path+'/'+str(year)
                    
        #Progra defensiva para no ingresar un evento que no se encuentra en el path
        try:
            dirs2 = os.listdir( path2 )
            E = True
        
        except FileNotFoundError:
            print("Evento "+str(name)+" no tiene la carpeta año")      
            return 0
    
        nday = dirs2[0]
    
        #Construimos el nombre del evento
        eventN = path+'/'+year+nday+hour
        text = []
        with open(eventN+".origin", 'r') as f:
            for i in f:
                if (i[0:4]!='-999'):
                    text.append(str(i[2:]))
                    
        #Cortamos los espacios en blanco para obtener solo la data
        data  = text[0].split("  ",36)
        data2 = text[0].split('    ')
        #Solo guardamos los primeros 4 datos: Lat, lon, prof, tiempo, magnitud
        #El tiempo se encuentra en un formato conocido como Unix Epoch
        dataF = (data[0],data[1],data[2],data[3],data2[-6])
        
        text2 = []
        #Abrimos un evento
        with open(eventN+".arrival", 'r') as f: 
            for i in f:
                #Filtramos los datos que nos interesan de origin
                a = str(i[0:75])
                a = a.split()
                #Quitamos la U y todos los arrivos 'del' o 'mL'
                if(len(a)==8 and a[7]!='del' and a[7]!='ml'):
                    text2.append(a) 
    
        #Almacenamos la estacion y el tiempo que les tomo llegar a la onda en listas separadas  
              
        #Almacenamos todas las ondas P 
        ListP = []
        #print("Ondas P: ")
        for i in range(len(text2)):
            if(text2[i][7]=='P'):
                x = -float(data[3])+float(text2[i][1])
                ListP.append((text2[i][0],x))
        #        print((text2[i][0],x))
        
        #Almacenamos todas las ondas S
        ListS = []
        #print("Ondas S: ")
        for i in range(len(text2)):
            if(text2[i][7]=='S'):
                x = -float(data[3])+float(text2[i][1])
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
    n_dat = []
    #Recorremos la lista de eventos
    for i in range(len(Eventos)):
        #Unimos/concatenamos el data Frame anterior al nuevo
        if(i!=0):
            dataF = event_stations_info_extractor(Eventos[i],n_dat,homeDir)
            #Se evita concatenar eventos cuando existe un error en las carpetas o no existe
            if(type(dataF) != int and type(dataO) != int):   
                dataO = pd.concat([dataO,dataF]) 
        #Solo en el caso 1 no actualizamos el dataFrame
        else:
            dataO = event_stations_info_extractor(Eventos[i],n_dat,homeDir)
    
    #Generamos un csv con todos los resultados.
    dataO.to_csv(homeDir+'/'+str(name)+'_estaciones.csv',index=True)
  
    
#Ejecución del programa
name = 'Mex_Sup'

if(False):
    Eventos = ["2019-03-05-1315",'2020-03-15-0122',"2020-04-22-2322","2020-04-07-1102"]
    homeDir = "C:/Users/HRV/Desktop/Post-U/Trabajo/Prueba/Data/Eventos/"
else:
    #Leemos los eventos que queremos analizar del informe anual 2 filtrado
    dfs = pd.read_csv('Data/Informe2A_Mex_Sup.csv')
    Env_names = dfs['folder']
    Eventos = []
    for envt in Env_names:
        Eventos.append(envt)
    homeDir = '/antelope/analysis/eventos/'

#Llamamos nuestra función        
events_station_extractor(Eventos,name,homeDir)