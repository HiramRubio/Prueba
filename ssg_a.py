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
from art import *
from AnimatedTry import *
from LeadTime import *

#Ejecución del programa
#Consola para imprimir mensajes en pantalla. 
console = Console()

#Variables Iniciales/Globales
name = ''
dfs = 'NONE'
Eventos = []
#homeDir = "C:/Users/HRV/Desktop/Post-U/Trabajo/Prueba/Data/Eventos/"
homeDir = '/antelope/analysis/eventos/'
#EventosD = ["2019-03-05-1315",'2019-11-14-0647','2020-03-06-0125']


#Verificamos que nuestro programa sea principal
if __name__ == "__main__":  
    #Menu con todas las opciones
    ACTIVE = True
    console.print(text2art('  ssg_a: Analisis Avanzado'), style="bold green")
    console.print('¡Bienvenido! Elige un [cyan]numero[/cyan] de las siguiente opciones:')
    while(ACTIVE):
        #Opciones
        console.print('1.   Extraer estaciones en base a un archivo')
        console.print('2.   Extraer estaciones de un evento')
        console.print('0.   [red]Salir[/red]')
        
        #Entrada del usuario
        a = input()
        
        #Verificación de entrada valida
        try:
            a = int(a)
        #Manejo de entrada incorrecta
        except ValueError:
            console.print('Entrada [red]NO[/red] valida')
            
        #Salida del Menu
        if(a == 0):
            ACTIVE = False
        #events = []
        
        #OPCION 1
        if(a ==1):
            ACTIVE2 = True
            CSV = False
            while(ACTIVE2):
                console.print('1.   Seleccionar archivo')
                console.print('2.   Filtrar ')
                console.print('3.   Mostrar eventos seleccionados ')
                console.print('4.   Generar Archivo ')
                console.print('5.   Lead Time ')
                console.print('0.   [red]Regresar[/red]')
                
                #Entrada del usuario
                b = input()
                
                #Verificación de entrada valida
                try:
                    b = int(b)
                #Manejo de entrada incorrecta
                except ValueError:
                    console.print('Entrada [red]NO[/red] valida')
                    
                #Salida del Menu
                if(b == 0):
                    ACTIVE2 = False
                    
                #Opcion 1-1   
                #Lectura de un archivo Pre-Procesado
                if(b == 1):
                    dfs = pd.read_csv('Data/Informe5A.csv')
                    console.print('Archivo Seleccionado: [blue]Informe6A[/blue]')
                    console.print('Fechas [blue]2019-03-01[/blue] -> [blue]2020-12-18[/blue]')
                
                #OPCION 1-2 No valida
                if(b == 2 and type(dfs) == str):
                    console.print('Archivo para trabajar aún [red]no[/red] selecionado')
                    
                #OPCION 1-2
                if(b ==2 and type(dfs) != str):
                    ACTIVE3 = True
                    while(ACTIVE3):
                        console.print('1.   Profundiad')
                        console.print('2.   Magnitud ')
                        console.print('3.   Zona SMG ')
                        console.print('4.   Zonas Profundidad ')
                        console.print('0.   [red]Regresar[/red]')
                        
                        #Entrada del usuario
                        c = input()
                        
                        #Verificación de entrada valida
                        try:
                            c = int(c)
                        #Manejo de entrada incorrecta
                        except ValueError:
                            console.print('Entrada [red]NO[/red] valida')
                            
                        #Salida del Menu
                        if(c == 0):
                            ACTIVE3 = False
                        #Filtro por protundidad
                        if(c == 1):
                            Eventos = range_finder(dfs,'prof',Eventos)
                        #Filtro por magnitud
                        if(c == 2):
                            Eventos = range_finder(dfs,'ml',Eventos)
                        #Filtro por zonas sismogeneticas
                        if(c == 3):
                            Eventos = zone_finder(dfs,'Zona',Eventos)
                        #Filtro por zonas de profundidad
                        if(c == 4):
                            Eventos = zone_finder(dfs,'Zona2',Eventos)
                
                #Opcion 1-3
                if(b == 3 and len(Eventos)!=0):
                    console.print(Eventos)
                    
                #Opcion 1-4 No valida
                if(b == 4 and len(Eventos)==0):
                    console.print('Eventos [red]no[/red] selecionados')
                    
                #Opcion 1-4
                if(b == 4 and len(Eventos)!=0):
                    console.print('Ingresar nombre del Archivo: ')
                    name = input()
                    events_station_extractor(Eventos,name,homeDir)
                    CSV = True
                    
                #Opcion 1-5 No valida
                if(b == 5 and CSV == False):
                    console.print('Archivo de estaciones [red]no[/red] generado')
                
                #Opcion 1-5 
                if(b == 5 and CSV == True):
                    Multiple_Lead_time(name, homeDir)
                    console.print('Archivo [blue]generado[/blue]')
                    
                    
        #OPCION 2
        if(a ==2):
            ACTIVE2 = True
            nombre = []
            while(ACTIVE2):
                console.print('1.   Extraer Informacion de evento')
                console.print('2.   Plot estaciones Evento ')
                console.print('3.   Plot arrivo a estaciones ')
                console.print('4.   Lead Time ')
                console.print('0.   [red]Regresar[/red]')
                
                #Entrada del usuario
                b = input()
                
                #Verificación de entrada valida
                try:
                    b = int(b)
                #Manejo de entrada incorrecta
                except ValueError:
                    console.print('Entrada [red]NO[/red] valida')
                    
                #Salida del Menu
                if(b == 0):
                    ACTIVE2 = False
                    
                #Opcion 2-1   
                if(b == 1):
                    x = input('Ingrese nombre del folder del evento: ')
                    nombre.append(x)
                    events_station_extractor(nombre,x,homeDir)
                    
                #Opcion 2-2 Error
                if(b == 2 and len(nombre)==0):
                    console.print('Archivo de evento [red]no[/red] generado')
                    
                #Opcion 2-2   
                if(b == 2 and len(nombre)>0):
                    event_plot_stations(nombre[0],homeDir)
                    
                #Opcion 3-2 Error
                if(b == 3 and len(nombre)==0):
                    console.print('Archivo de evento [red]no[/red] generado')
                    
                #Opcion 3-2   
                if(b == 3 and len(nombre)>0):
                    #event_plot_stations(nombre[0],homeDir)
                    Animate_event(nombre[0], homeDir)
                    console.print('Video generado', style="bold green")
                    
                #Opcion 4-2 Error
                if(b == 4 and len(nombre)==0):
                    console.print('Archivo de evento [red]no[/red] generado')
                    
                #Opcion 4-2   
                if(b == 4 and len(nombre)>0):
                    #event_plot_stations(nombre[0],homeDir)
                    LT = Lead_time2(nombre[0],homeDir)
                    console.print('Lead time: '+str(LT[3]-LT[1])+', entre '+LT[0]+' ,'+LT[2], style="bold green")
                    
            
    console.print(text2art(' :)  '), style="bold blue")
    #dfs = pd.read_csv('Data/Informe2A.csv')
    #Eventos = range_finder(dfs,'prof',events)
    #events_station_extractor(Eventos,name,homeDir)
    
