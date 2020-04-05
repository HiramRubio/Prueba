# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 02:47:33 2020

@author: Steven Rubio
Determinar la region SMG (GT) de un sismo. 
"""


def Det_Region(xpo,ypo):
    
    """
    Variables de entrada:
    xpo: longitud
    ypo: latitud
    
    Variable de retorno:
    Region: Nombre de la región SMG
    
    Librerias necesarias
    """
    from mpl_toolkits.basemap import Basemap
    from pointInside import is_inside_sm
    import time
    
    #Tiempo de ejecucion 0
    t = time.perf_counter() 
    
    #Definimos la región de nuestro mapa
    x1,x2 = -86.4616, -95.0688
    y1,y2 = 17.7475, 11.8971
    
    #Creamos la instancia de la proyección que vamos a utilizar. 
    mp = Basemap(resolution='i', # c, l, i, h, f or None
            projection='merc', 
            lat_0=14.6569, lon_0=-90.51,
            llcrnrlon=x2+0.1, llcrnrlat=y2-0.1,urcrnrlon=x1-0.1, urcrnrlat=y1+0.1)
    #Leemos la ShapeFile con las regiones SMG de GT
    mp.readshapefile('Data/ale/ZONASSISMOMOD', 'ej3',drawbounds=False)
    #Nombre de las zonas. 
    Zonas = ['G1','S1','G2-S2','S3','G3','G4','G5-S4-H1','G6','G8']

    #Leemos todas la regiones de nuestra SF
    for info, shape in zip(mp.ej3_info, mp.ej3):
    #Hacemos un ciclo para corroborar si un sismo esta en cada zona
        for j in range(len(Zonas)):
            #Evaluamos cada Zona
            if info['ZONA'] == Zonas[j]:
                patches3 = []
                x, y = zip(*shape)
                for i in range(len(x)):
                    patches3.append((x[i],y[i]))
                #Mapeo del punto de prueba a nuestra proyección
                xpt,ypt = mp(xpo,ypo)
                testP = (xpt,ypt)
                #Determinamos si se encuentra dentro de la region Valuada
                if (is_inside_sm(patches3,testP)):
                    print("Execution time: " + str(time.perf_counter() - t)) 
                    return Zonas[j]
                #Si no, retornamos un SC
                else:
                    Region = "SC"
                patches3 = []
                
    print("Execution time: " + str(time.perf_counter() - t)) 
    return Region

#Prueba
import pandas as pd
dfs = pd.read_csv('Data/Anual2019.csv')
for i in range(len(dfs)):
    xpo = dfs[' lon'][i]
    ypo = dfs[' lat'][i]
    Reg = Det_Region(xpo,ypo)
    print("Sismo ",i,". Lon: ", xpo, "Lat: ",ypo, "Region: ",Reg)
            
