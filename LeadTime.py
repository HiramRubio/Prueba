# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 02:43:17 2020

@author: Steven Hiram
"""

def Estacion_Capital(Estat):
    # ----------
    # Entradas:
    # Estat     = Nombre de la estación
    # ----------
    # Salidas:
    # val       = Booleano para indicar si esta o no en la capital 
    # -------
    
    #Declaración e inialización de variable
    val = False
    #Estaciones consideradas en la capital
    CIUDAD = ['CIRS','VILL','SJPIN','CMONM','CINGE','CSTER','CASUN','KINAL',
              'ITC','JUAMA','EXCEL','CCONS','IPRES','TADEO','CBIL','CAUST',
              'LSECB','ICREY','ACRIS','SEUNI','ASEGG','CSAGC','AMGGT','LGUAT',
              'CDBOS','RGIL','JUNKA','CEPRO','NRNJO','SMP','SPAYM','BVH','ALUX',
              'TUC','VILLC','MERCK','RCACE']
    #Busqueda de estación 
    if(Estat in CIUDAD):   val = True
    return val

def Lead_time(folder,homeDir,PRINT = False,READ = True):
    # ----------
    # Entradas:
    # folder    = Nombre del evento
    # homeDir   = Directorio con eventos
    # PRINT     = Bandera para prints
    # READ      = Bandera para leer csv o usar el archivo proporcionado como parametro
    # ----------
    # Salidas:
    # list       = Lista con estaciones y tiempos de arrivo 
    # -------
    
    #Librerias
    import pandas as pd 
    
    #Leemos el archivo con las estaciones del evento
    if(READ):   
        est = pd.read_csv(homeDir+str(folder)+'_estaciones.csv')
        est.sort_values(by = ['DeltaT (segundos)'], inplace=True)
    #LLamada con folder ya filtrado
    else:       est = folder
    
    
    #Filtramos para buscar primer arrivo P
    estP = est[est['Onda'].isin(['P'])] 
    #Declaración e inialización de variables
    timeP ,est_P = 0.0,'NONE'
    
    #Recorrido de estaciones y tiempo de arrivo
    #Se revisa que sea un arrivo P que no esté en la capital
    for a,b in zip(estP['Est'],estP['DeltaT (segundos)']):
        #Sustitucion en primer caso 
        if(timeP == 0.0 and Estacion_Capital(a) == False):   timeP ,est_P = b, a


    #Filtramos para buscar primer arrivo S
    estS = est[est['Onda'].isin(['S'])]
    #Declaración e inialización de variables
    timeS, est_S = 0.0, 'NONE'
   
    #Recorrido de estaciones y tiempo de arrivo
    #Se revisa que sea un arrivo S esté en la capital
    for a,b in zip(estS['Est'],estS['DeltaT (segundos)']):
        #Sustitucion en primer caso 
        if(timeS == 0.0 and Estacion_Capital(a)):   timeS ,est_S = b, a
    
    if(PRINT):
        if(timeP != 0.0 and timeS != 0.0):  
            #Evento en la Capital
            if(timeS-timeP < 0.0):  print('Evento en la Capital.','Lead time: '+str(timeS-timeP)+', entre '+est_P+' ,'+est_S)
            #Evento buscado
            else:                   print('Lead time: '+str(timeS-timeP)+', entre '+est_P+' ,'+est_S)
        
        #En caso que no se encuentre una P fuera de la capital o una S en la capital    
        else:   print('No es posible calcular')
    
    return (est_P, timeP, est_S, timeS)


# Funcion que retorna el tiempo de arrivo
def myFunc(e):
  return e['DeltaT (segundos)']


def Lead_time2(folder, homeDir,PRINT = False,READ = True):
    # ----------
    # Entradas:
    # folder    = Nombre del evento
    # homeDir   = Directorio con eventos
    # PRINT     = Bandera para prints
    # READ      = Bandera para leer csv o usar el archivo proporcionado como parametro
    # ----------
    # Salidas:
    # list       = Lista con estaciones y tiempos de arrivo 
    # -------
    
    #Librerias
    import pandas as pd 
    
    #Leemos el archivo con las estaciones del evento
    if(READ):   est = pd.read_csv(homeDir+str(folder)+'_estaciones.csv')
    #LLamada con folder ya filtrado
    else:       est = folder
    #Filtramos para buscar primer arrivo P
    estP = est[est['Onda'].isin(['P'])] 
    #Declaración e inialización de variables
    timeP ,est_P = 0.0,'NONE'
    
    #Ordeno las listas en base al tiempo de arrivo
    listT, listN = (list(t) for t in zip(*sorted(zip(estP['DeltaT (segundos)'].tolist(), estP['Est'].tolist()))))
    
    #Recorrido de estaciones y tiempo de arrivo
    #Se revisa que sea un arrivo P que no esté en la capital
    #Se rompre al encontrar el primer caso
    for a,b in zip(listN,listT):
       if(timeP == 0.0 and Estacion_Capital(a) == False):   
        timeP ,est_P = b, a 
        break

    #Filtramos para buscar primer arrivo P
    estS = est[est['Onda'].isin(['S'])]
    #Declaración e inialización de variables
    timeS, est_S = 0.0, 'NONE'
   
    #Ordeno las listas en base al tiempo de arrivo
    listT, listN = (list(t) for t in zip(*sorted(zip(estS['DeltaT (segundos)'].tolist(), estS['Est'].tolist()))))
    
    #Recorrido de estaciones y tiempo de arrivo
    #Se revisa que sea un arrivo S que este en la capital
    #Se rompre al encontrar el primer caso
    for a,b in zip(listN,listT):
       if(timeS == 0.0 and Estacion_Capital(a) == True):   
        timeS ,est_S = b, a 
        break
    
    #print(est_S,timeS)
    if(PRINT):
        if(timeP != 0.0 or timeS != 0.0):  
            #Evento en la Capital
            if(timeS-timeP < 0.0):  print('Evento en la Capital.','Lead time: '+str(timeS-timeP)+', entre '+est_P+' ,'+est_S)
            #Evento buscado
            else:                   print('Lead time: '+str(timeS-timeP)+', entre '+est_P+' ,'+est_S)
        
        #En caso que no se encuentre una P fuera de la capital o una S en la capital    
        else:   print('No es posible calcular')
    
    return (est_P, timeP, est_S, timeS)



def Multiple_Lead_time(name, homeDir,METHOD = False):
    # ----------
    # Entradas:
    # name      = Nombre del archivo a leer
    # homeDir   = Directorio con eventos
    # METHOD    = Bandera para cambiar entre 2 metodos
    # ----------
    # Salidas:
    # Archivo .csv
    # -------
    
    #Librerias
    import pandas as pd 
    import numpy as np
    
    #Leemos el archivo con las estaciones del evento
    ests = pd.read_csv(homeDir+str(name)+'.csv')
    #Obtenemos el nombre de todos los folders
    events_names = np.unique(ests['Folder'])
    
    dataLT = []
    for element in events_names:
        #Filtramos el evento a analizar
        eventN = ests[ests['Folder'].isin([str(element)])]
        #Metodos alternativos para calcular el LeadTime
        if(METHOD): eventD = Lead_time(eventN,homeDir,False,False)
        else:       eventD = Lead_time2(eventN,homeDir,False,False)
        dataLT.append((element,eventD[3]-eventD[1],eventD[0],eventD[2]))
    
    #Conversion a DataFrame
    dataO = pd.DataFrame(dataLT,columns=['Folder','LeadTime','EstacionP','EstacionS'])
    dataO.to_csv(homeDir+'/'+str(name)+'_LeadTime.csv',index=True)
    
    
#homeDir = "C:/Users/HRV/Desktop/Post-U/Trabajo/Prueba/Data/Eventos/"
#name = "Mag4_estaciones"