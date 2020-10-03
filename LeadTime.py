# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 02:43:17 2020

@author: Steven Hiram
"""

def Estacion_Capital(Estat):
    
    val = False
    CIUDAD = ['CIRS','VILL','SJPIN','CMONM','CINGE','CSTER','CASUN','KINAL',
              'ITC','JUAMA','EXCEL','CCONS','IPRES','TADEO','CBIL','CAUST',
              'LSECB','ICREY','ACRIS','SEUNI','ASEGG','CSAGC','AMGGT','LGUAT',
              'CDBOS','RGIL','JUNKA','CEPRO','NRNJO','SMP','SPAYM','BVH','ALUX',
              'TUC','VILLC','MERCK','RCACE']
    if(Estat in CIUDAD):   val = True
    return val

def Lead_time(folder, homeDir):
    import pandas as pd 
    
    #Leemos el archivo con las estaciones del evento
    est = pd.read_csv(homeDir+str(folder)+'_estaciones.csv')
    #Primer arrivo P
    estP = est[est['Onda'].isin(['P'])]
    #print(estP)  
    timeP = 0.0
    est_P = ''
    for a,b in zip(estP['Est'],estP['DeltaT (segundos)']):
        if(timeP == 0.0 and Estacion_Capital(a) == False):   
            timeP ,est_P = b, a
           
        else:
            if(b < timeP and Estacion_Capital(a) == False): 
                timeP ,est_P = b, a

    
    #Primer arrivo S
    estS = est[est['Onda'].isin(['S'])]
    #print(estS)
    timeS = 0.0
    est_S = ''
    for a,b in zip(estS['Est'],estS['DeltaT (segundos)']):
        if(timeS == 0.0 and Estacion_Capital(a)):   timeS ,est_S = b, a
        else:
            if(b < timeS and Estacion_Capital(a)):  timeS ,est_S = b, a
    #print(est_S,timeS)
    if(timeP != 0.0 or timeS != 0.0):  
        if(timeS-timeP < 0.0):  print('Evento en la Capital.','Lead time: '+str(timeS-timeP)+', entre '+est_P+' ,'+est_S)
        else:                   print('Lead time: '+str(timeS-timeP)+', entre '+est_P+' ,'+est_S)
        
    else:   print('No es posible calcular')
    
homeDir = "C:/Users/HRV/Desktop/Post-U/Trabajo/Prueba/Data/Eventos/"
folderP = '2019-11-13-1628'

Lead_time(folderP,homeDir)
Lead_time('2019-11-14-0647',homeDir)
Lead_time('2020-04-19-0821',homeDir)
Lead_time('2020-07-15-2054',homeDir)