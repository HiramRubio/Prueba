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

def Lead_time(folder, homeDir):
    # ----------
    # Entradas:
    # folder    = Nombre del evento
    # homeDir   = Directorio con eventos
    # ----------
    # Salidas:
    # list       = Lista con estaciones y tiempos de arrivo 
    # -------
    import pandas as pd 
    
    #Leemos el archivo con las estaciones del evento
    est = pd.read_csv(homeDir+str(folder)+'_estaciones.csv')
    #Filtramos para buscar primer arrivo P
    estP = est[est['Onda'].isin(['P'])] 
    #Declaración e inialización de variables
    timeP ,est_P = 0.0,''
    
    #Recorrido de estaciones y tiempo de arrivo
    #Se revisa que sea un arrivo P que no esté en la capital
    for a,b in zip(estP['Est'],estP['DeltaT (segundos)']):
        #Sustitucion en primer caso 
        if(timeP == 0.0 and Estacion_Capital(a) == False):   
            timeP ,est_P = b, a
        #Actualización de casos  
        else:
            if(b < timeP and Estacion_Capital(a) == False): 
                timeP ,est_P = b, a

    #Filtramos para buscar primer arrivo P
    estS = est[est['Onda'].isin(['S'])]
    #Declaración e inialización de variables
    timeS, est_S = 0.0, ''
   
    #Recorrido de estaciones y tiempo de arrivo
    #Se revisa que sea un arrivo S esté en la capital
    for a,b in zip(estS['Est'],estS['DeltaT (segundos)']):
        #Sustitucion en primer caso 
        if(timeS == 0.0 and Estacion_Capital(a)):   timeS ,est_S = b, a
        #Actualización de casos 
        else:
            if(b < timeS and Estacion_Capital(a)):  timeS ,est_S = b, a
    #print(est_S,timeS)
    if(timeP != 0.0 or timeS != 0.0):  
        #Evento en la Capital
        if(timeS-timeP < 0.0):  print('Evento en la Capital.','Lead time: '+str(timeS-timeP)+', entre '+est_P+' ,'+est_S)
        #Evento buscado
        else:                   print('Lead time: '+str(timeS-timeP)+', entre '+est_P+' ,'+est_S)
    
    #En caso que no se encuentre una P fuera de la capital o una S en la capital    
    else:   print('No es posible calcular')
    
    return (est_P, timeP, est_S, timeS)
    
homeDir = "C:/Users/HRV/Desktop/Post-U/Trabajo/Prueba/Data/Eventos/"
folderP = '2019-11-13-1628'

Lead_time(folderP,homeDir)
Lead_time('2019-11-14-0647',homeDir)
Lead_time('2020-04-19-0821',homeDir)
Lead_time('2020-07-15-2054',homeDir)