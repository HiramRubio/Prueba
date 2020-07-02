# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 02:08:28 2020

@author: Steven

Prueba de función para abrir el csv de estaciones extraer los eventos dados ciertos parametros
"""

import pandas as pd
import numpy as np

#Importamos el archivo
dfs = pd.read_csv('Data/Informe2A.csv')

'''
names  = dfs['folder']
zones  = dfs['Zona']
zones2 = dfs['Zona2']
mag    = dfs['ml']

#Buscador por zona 

#Lista de zonas 1 disponibles
i = 0
x = np.unique(zones)
for a,b in zip(names,zones):
    if(b == x[4]): 
        #print(a)
        i = i+1
print(i)
'''

def zone_finder(dfs):
    
    #Lista de eventos
    Eventos = []
    x = dfs.columns
    #Validación de que el archivo que estamos utilizando contiene la clasificación zone
    if 'Zona' in x:
        print('Archivo utilizable')
        
        #Se muestran las opciones
        zones  = dfs['Zona']
        opc = []
        opc_names = np.unique(zones)
        var = True
        #Ciclo para seleccionar zona o zonas
        print('Opciones Disponibles')
        print(opc_names)
        while(var):
            a = input('Ingrese la zona a clasificar, Done, Zonas o Selec (Seleccionados): ')
            if(len(opc)==len(opc_names)):
                print('Todas las Zonas seleccionadas, ejecutando busqueda')
                var = False
            if(a == 'Done'): 
                if(len(opc)== 0): 
                    print('Ninguna Zona seleccionada')
                else: 
                    var = False  
            if(a == 'Zonas'):   
                print(opc_names)
                pass
            
            if(a == 'Selec'):   
                print(opc)
            else:
                if(a in opc_names): 
                    if(a in opc):   print('Opcion ya seleccionada')
                    else:           opc.append(a)
                else: 
                    if(a!='Zonas' and len(opc)!=len(opc_names)): print('Opcion no valida')
                
        print('Zonas seleccionadas')
        print(opc)
        #Nombre de los eventos
        names  = dfs['folder']
        i = 0
        #Buscamos los folders que cuenten con 
        for a,b in zip(names,zones):
            if(b in opc): 
                Eventos.append(a)
                i = i+1
        print("Cantidad de eventos localizados: "+str(i))
        print(Eventos)
        
        
    else:
        print('Archivo no contiene columna Zona ')