# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 04:28:36 2020

@author: Steven Rubio

Programa Maestro  para ejecucion de otras funciones:
- Extraccion de Estaciones de un evento
- Extraccion de Estaciones de multiples eventos
"""
import pandas as pd
from rich.console import Console
from folders_finder import *
from stations_extractor import * 

#Ejecución del programa

#Consola para imprimir mensajes en pantalla. 
console = Console()

name = 'Prueba_0_prof'

if(False):
    #Eventos = ["2019-03-05-1315",'2020-03-15-0122',"2020-04-22-2322","2020-04-07-1102","2020-04-07-1122","2019-05-12-2356","2019-05-13-0150"]
    EventosD = ["2019-03-05-1315",'2019-11-14-0647','2020-03-06-0125']
    homeDir = "C:/Users/HRV/Desktop/Post-U/Trabajo/Prueba/Data/Eventos/"
else:
    #Leemos los eventos que queremos analizar del informe anual 2 filtrado
    dfs = pd.read_csv('Data/Informe2A_Mex_Sup.csv')
    Env_names = dfs['folder']
    Eventos = []
    for envt in Env_names:
        Eventos.append(envt)
    homeDir = '/antelope/analysis/eventos/'

#Verificamos que nuestro programa sea principal
if __name__ == "__main__":  
    #Leemos un archivo con todos los filtros
    events = []
    dfs = pd.read_csv('Data/Informe2A.csv')
    Eventos = range_finder(dfs,'prof',events)
    events_station_extractor(Eventos,name,homeDir)
