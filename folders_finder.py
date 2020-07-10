# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 02:08:28 2020

@author: Steven

Prueba de función para abrir el csv de estaciones extraer los eventos dados ciertos parametros
"""

import pandas as pd
import numpy as np
from rich.console import Console


#Importamos el archivo
#dfs = pd.read_csv('Data/Informe2A.csv')
#Consola para imprimir mensajes en pantalla. 
console = Console()
#console.print()

def zone_finder(dfs,column,events):
    # ----------
    # Entradas:
    # dfs       = Archivo csv a trabajar
    # column    = Columna utilizada para filtrar
    # events    = Eventos ya filtrados
    # ----------
    # Salidas:
    # Eventos   = Lista con los eventos clasificados
    # ----------    
    
    #Variable de control
    PRINT = False
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
        console.print("Cantidad de eventos seleccionados: "+str(len(Eventos)))
        #Retornamos los eventos que cumplieron
        if(PRINT):  console.print(Eventos)
        
        #Verificamos si se posee una busqueda previa
        if(len(events)>0):
            #Buscamos los elementos que se encuentran en la lista ingresada
            for elemnt in Eventos:
                if (elemnt in events):  
                    pass
                #Si un elemento no se encuentra se muestra y quita
                else:   
                    if(PRINT):  console.print('Evento [bold red]no [/bold red]encontrado: '+elemnt)
                    Eventos.remove(elemnt)
                
            #Conteo de eventos filtrados
            console.print("Cantidad de eventos con [bold cyan]ambos [/bold cyan]filtros: "+str(len(Eventos)))
            #Retornamos los eventos que cumplieron
            if(PRINT):  console.print(Eventos)
        return(Eventos)
        
        
    else:
        #En caso de que el archivo no conenta la columna que especificamos
        #Returnomos un False
        console.print('Archivo no contiene columna Zona ', style="bold red")
        return(False)
    
#--------------------------//-----------------------

def range_finder(dfs,column,events):
    # ----------
    # Entradas:
    # dfs       = Archivo csv a trabajar
    # column    = Columna utilizada para filtrar
    # events    = Eventos ya filtrados
    # ----------
    # Salidas:
    # Eventos   = Lista con los eventos clasificados
    # ----------    
    
    #Variable de control
    PRINT = False
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
        
    
        inpA = input('Ingrese el valor minimo: ')
        while(var):
            inpB = input('Ingrese el valor máximo: ')
            if(float(inpB) > float(inpA)):   var = False
            else:   console.print('Rango no valido')
            
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
        console.print("Cantidad de eventos seleccionados: "+str(len(Eventos)))
        #Retornamos los eventos que cumplieron
        if(PRINT):  console.print(Eventos)
        
        #Verificamos si se posee una busqueda previa
        if(len(events)>0):
            #Buscamos los elementos que se encuentran en la lista ingresada
            for elemnt in Eventos:
                if (elemnt in events):  
                    pass
                #Si un elemento no se encuentra se muestra y quita
                else:   
                    if(PRINT):  console.print('Evento [bold red]no [/bold red]encontrado: '+elemnt)
                    Eventos.remove(elemnt)
                
            #Conteo de eventos filtrados
            console.print("Cantidad de eventos con [bold cyan]ambos [/bold cyan]filtros: "+str(len(Eventos)))
            #Retornamos los eventos que cumplieron
            if(PRINT):  console.print(Eventos)
        return(Eventos)
        
    else:
        #En caso de que el archivo no conenta la columna que especificamos
        #Returnomos un False
        console.print('Archivo no contiene columna Zona ', style="bold red")
        return(False)    
 
#Filtro 21.5 - 22.5 prof
Eventos_Prueba = [
    '2019-08-27-0339',
    '2019-09-30-0427',
    '2019-12-21-1809',
    '2020-01-31-1311',
    '2019-06-05-0925',
    '2019-09-13-0827',
    '2020-02-03-0722',
    '2019-12-28-0905',
    '2019-02-02-1710',
    '2019-06-23-0530',
    '2019-08-26-0950',
    '2019-10-26-0921',
]

#zone_finder(dfs,'Zona',Eventos_Prueba)
#range_finder(dfs,'prof',Eventos_Prueba)
