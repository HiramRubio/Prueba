# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 04:40:10 2020

@author: Steven Rubio
Abrir un evento y extraer si información solo con el nombre del evento

Prueba
"""
import os, sys

#Eventos
Eventos = ["2019-03-05-1315",'2020-03-15-0122',"2020-04-22-2322"]


#def event_stations_info_extractor(Evento):
      
name    = Eventos[0]
year    = name[0:4]
month   = name[5:7]
day     = name[8:10]
hour    = name[11:16]

#Definimos el directorio madre y abrimos el evento
path = "C:/Users/HRV/Desktop/Post-U/Trabajo/Prueba/Data/Eventos/"+str(year)+'/'+str(month)+'/'+str(name)
E = False

#Progra defensiva para no ingresar un evento que no se encuentra en el path
try:
    dirs = os.listdir( path )
    E = True

except FileNotFoundError:
    print("Evento no existe")            
   
if(E):
    
    #Obtenemos el día del año del evento
    path2 = path+'/'+str(year)
    # This would print all the files and directories
    dirs2 = os.listdir( path2 )
    nday = dirs2[0]

    #Construimos el nombre del evento
    eventN = path+'/'+year+nday+hour
    text = []
    with open(eventN+".origin", 'r') as f:
        for i in f:
            if (i[0:4]!='-999'):
                text.append(str(i[2:]))
                
    #Cortamos los espacios en blanco para obtener solo la data
    data = text[0].split("  ",36)
    #Solo guardamos los primeros 4 datos: Lat, lon, prof, tiempo, magnitud
    #El tiempo se encuentra en un formato conocido como Unix Epoch
    data = (data[0],data[1],data[2],data[3],data[32])
    print(data)

            