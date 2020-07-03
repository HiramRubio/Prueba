# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 02:08:28 2020

@author: Steven

Prueba de función para abrir el csv de estaciones extraer los eventos dados ciertos parametros
"""

import pandas as pd
import numpy as np
#from rich import print
from rich.console import Console
#from rich.progress import track

#Importamos el archivo
dfs = pd.read_csv('Data/Informe2A.csv')
#Consola para imprimir mensajes en pantalla. 
console = Console()
console.print()

def zone_finder(dfs,column):
    # ----------
    # Entradas:
    # dfs       = Archivo csv a trabajar
    # column    = Columna utilizada para filtrar
    # ----------
    # Salidas:
    # Eventos   = Lista con los eventos clasificados
    # ----------    
    

    #Columnas con las que el método funciona
    opc_val = ['Zona','Zona2']
    #Lista de eventos
    Eventos = []
    #Columnas disponibles en el csv
    x = dfs.columns
    #Validación de que el archivo que estamos utilizando contiene la clasificación zone
    if( column in x and column in opc_val):
        console.print('Archivo utilizable', style="bold green")
        
        #Se muestran las opciones
        zones  = dfs[column]
        opc = []
        opc_names = np.unique(zones)
        var = True
        #Ciclo para seleccionar zona o zonas
        
        console.print('Opciones Disponibles')
        console.print(opc_names)
        while(var):
            #Entrada No Valida: El usuario intenta ingresar más zonas de las presentadas, automáticamente
            #sale del ciclo con todas las opciones
            if(len(opc)==len(opc_names)):
                console.print('[bold green]Todas las Zonas seleccionadas !![/bold green]. Ejecutando busqueda')
                var = False
            #Entrada dle usuario
            if(var):    a = input('Ingrese la zona a clasificar, Done, Zonas o Selec (Seleccionados): ')
            #Salida del ciclo, esta es válida si se tiene al menos una opcion seleccionada
            if(a == 'Done'): 
                if(len(opc)== 0): 
                    console.print('Ninguna Zona seleccionada', style="bold red")
                else: 
                    var = False  
            #Impresión de Zonas disponibles para clasificcion
            if(a == 'Zonas'):   
                console.print(opc_names)
            #Impresión de Zonas seleccionadas hasta el momento
            if(a == 'Selec'):   
                console.print(opc)
            else:
                if(a in opc_names): 
                    #Entrada no Valida: Una opcion repetida
                    if(a in opc and var):   console.print('Opcion ya seleccionada',style='bold magenta')
                    else:           opc.append(a)
                else: 
                    #Entrada no valida: Una opcion no valida, entre otras
                    if(a!='Zonas' and len(opc)!=len(opc_names) and a != 'Done'): console.print('Opcion no valida',style='bold red')
                
        console.print('Zonas seleccionadas')
        console.print(opc)
        #Nombre de los eventos del csv
        names  = dfs['folder']
        i = 0
        #Buscamos los folders que cuenten con 
        for a,b in zip(names,zones):
            if(b in opc): 
                Eventos.append(a)
                i = i+1
                
        #Conteo de eventos
        console.print("Cantidad de eventos seleccionados: "+str(i))
        #Retornamos los eventos que cumplieron
        return(Eventos)
        
        
    else:
        #En caso de que el archivo no conenta la columna que especificamos
        #Returnomos un False
        console.print('Archivo no contiene columna Zona ', style="bold red")
        return(False)
    
#--------------------------//-----------------------

def range_finder(dfs,column):
    # ----------
    # Entradas:
    # dfs       = Archivo csv a trabajar
    # column    = Columna utilizada para filtrar
    # ----------
    # Salidas:
    # Eventos   = Lista con los eventos clasificados
    # ----------    
    

    #Columnas con las que el método funciona
    opc_val = ['prof','ml']
    #Lista de eventos
    Eventos = []
    #Columnas disponibles en el csv
    x = dfs.columns
    #Validación de que el archivo que estamos utilizando contiene la clasificación zone
    if( column in x and column in opc_val):
        console.print('Archivo utilizable', style="bold green")
        
        #Se muestran las opciones
        values  = dfs[column]
        opc = []
        minV,maxV = min(values),max(values)
        var = True
        #Ciclo para seleccionar zona o zonas
        
        console.print('Rango Disponible')
        console.print('('+str(minV)+' ,'+str(maxV)+')')
        
        while(var):
            inpA = input('Ingrese el valor minimo: ')
            inpB = input('Ingrese el valor máximo: ')
            var = False
            
        console.print(opc)
        #Nombre de los eventos del csv
        names  = dfs['folder']
        i = 0
        #Buscamos los folders que cuenten con 
        for a,b in zip(names,values):
            if(b >= float(inpA) and b <= float(inpB)): 
                Eventos.append(a)
                i = i+1
                
        #Conteo de eventos
        console.print("Cantidad de eventos seleccionados: "+str(i))
        #Retornamos los eventos que cumplieron
        console.print(Eventos)
        
        
    else:
        #En caso de que el archivo no conenta la columna que especificamos
        #Returnomos un False
        console.print('Archivo no contiene columna Zona ', style="bold red")
        return(False)    
    
#zone_finder(dfs,'Zona')
range_finder(dfs,'prof')