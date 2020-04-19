# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 04:03:41 2020

@author: Steven Rubio
Determinar el departamento y municipio de un sismo.
"""
def Det_Mun(ypo,xpo):
    
    """
    Variables de entrada:
    xpo: longitud
    ypo: latitud
    
    Variable de retorno:
    Region: Nombre del Municipio
    
    Librerias necesarias
    """
    from mpl_toolkits.basemap import Basemap
    from pointInside import is_inside_sm
    import time
    
    #Variable de Control 
    Mostrar=False
    #Tiempo de ejecucion 0
    if(Mostrar):t = time.perf_counter() 
    
    #Definimos la región de nuestro mapa
    x1,x2 = -86.4616, -95.0688
    y1,y2 = 17.7475, 11.8971
    
    #Creamos la instancia de la proyección que vamos a utilizar. 
    mp = Basemap(resolution='i', # c, l, i, h, f or None
            projection='merc', 
            lat_0=14.6569, lon_0=-90.51,
            llcrnrlon=x2+0.1, llcrnrlat=y2-0.1,urcrnrlon=x1-0.1, urcrnrlat=y1+0.1)
    #Leemos la ShapeFile con los municipios de GT
    #Esta data se obtuvo de Conred*
    mp.readshapefile('Data/gtm/gtm_admbnda_adm2_ocha_conred_20190207', 'ej2',drawbounds=False)

    #Leemos todos los municipios
    for info, shape in zip(mp.ej2_info, mp.ej2):
    #Hacemos un ciclo para corroborar si un sismo esta en este municipio
        for j in range(len(info['ADM2_REF'])):
          
            patches3 = []
            x, y = zip(*shape)
            for i in range(len(x)):
                patches3.append((x[i],y[i]))
            #Mapeo del punto de prueba a nuestra proyección
            xpt,ypt = mp(xpo,ypo)
            testP = (xpt,ypt)
            #Determinamos si se encuentra dentro de la region Valuada
            if (is_inside_sm(patches3,testP)):
                if(Mostrar): print("Execution time: " + str(time.perf_counter() - t)) 
                return info['ADM2_REF']
            #Si no, retornamos un SC
            else:
                Region = "SC"
            patches3 = []
               
                

    if(Mostrar): print("Execution time: " + str(time.perf_counter() - t)) 
    return Region

#Prueba de datos
if(False):
    import pandas as pd
    dfs = pd.read_csv('Data/Anual2019.csv')
    for i in range(740,840):
        xpo = dfs[' lon'][i]
        ypo = dfs[' lat'][i]
        Mun = Det_Mun(ypo,xpo)
        print("Sismo ",i,"Lat: ",ypo,". Lon: ", xpo, "Mun: ",Mun)