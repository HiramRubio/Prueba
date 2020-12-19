# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 02:48:57 2020

@author: Hiram

Aprendiendo a hacer imagenes animadas
de las estaciones que detectaron un evento en específico
"""
import pandas as pd 

def Animate_event(folder, homeDir,EXPECTED = True):
    
    
    #Leemos el archivo con las estaciones del evento
    est = pd.read_csv(homeDir+str(folder)+'_estaciones.csv')
    
    #Librerias
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
    from mpl_toolkits.basemap import Basemap
    import math
    from stations_extractor import event_info_extractor
    import numpy as np
    
    #Inicio de plot
    fig, ax = plt.subplots(figsize=(8,8))
    #Nacional
    m = Basemap(resolution='i', # c, l, i, h, f or None
        lat_0=14.6569, lon_0=-90.51,
        llcrnrlon=-92.93, llcrnrlat=13.15,urcrnrlon=-87.58, urcrnrlat=18.42,epsg=4326,
        projection='tmerc')
    
    #Cargamos el "fondo# del mapa
    m.arcgisimage(service='World_Terrain_Base', xpixels=1600, dpi=210,verbose= True)    
    #m.drawmapboundary(fill_color='#46bcec')                  
    #m.fillcontinents(color='#f2f2f2',lake_color='#46bcec')
    #Leemos nuestra shapefile, no los activamos todos
    m.readshapefile('Data/gtm/gtm_admbnda_adm0_ocha_conred_20190207', 'ej0',linewidth=1.5)
    m.readshapefile('Data/gtm/gtm_admbnda_adm1_ocha_conred_20190207', 'ej1',linewidth=0.5)
    
    #Directorio con data del evento
    #homeDir = "C:/Users/HRV/Desktop/Post-U/Trabajo/Prueba/Data/Eventos/"
    
    #Data principal del evento
    data = event_info_extractor(folder,homeDir)
    
    #Tiempo máximo
    t_max =math.ceil(max(est['DeltaT (segundos)']))+2
          
    # initialization function 
    def init(): 
        #Ingreo de nombres de estaciones que se desean poner en la gráfica
        print('Estaciones disponibles: ')
        print(np.unique(est['Est']))
        Names = input("Ingrese el nombre de las estaciones a gráficar (Entre comillas y separadas por coma): ")
        #Texto/Leyenda
        ax.plot(-89.00,17.0,'s',marker='^',color='r', markersize=6)
        ax.plot(-89.00,16.8,'s',marker='^',color='g', markersize=6)
        ax.text(-88.90,16.97,'Onda P', fontsize=8,bbox=dict(boxstyle = "square",
                  facecolor = "white"))
        ax.text(-88.90,16.77,'Onda S', fontsize=8,bbox=dict(boxstyle = "square",
                  facecolor = "white"))
        #Plot epicentro
        x,y = m(float(data[1]),float(data[0]))
        plot = ax.plot(x,y,'s',marker='*',color='k', markersize=10,markeredgecolor = 'k')
        #Plot de las estaciones sin color
        for lat,lon,name in zip(est['Lat'],est['Lon'],est['Est']):
            x,y = m(lon,lat)
            plot = ax.plot(x,y,'s',marker='^',color='none', markersize=10,markeredgecolor = 'k')
            #Plot del nombre de algunas estaciones
            if name in Names:
                ax.text(x+0.01,y+0.07,name,fontsize=8,color='m',rotation=45,bbox=dict(boxstyle = "square",
                  facecolor = "white"))
                
        return plot
    
    #Funcion para generar puntos esperados de onda
    def expected_wave_points(xo,yo,est):
        # ----------
        # Entradas:
        # xo,yo     = Coordenadas del evento
        # est       = Archivo .csv con datos del evento
        # ----------
        # Salidas:
        # x_e_p,y_e_p   = Coordenadas de onda esperadas
        # time_e        = Lista con los tiempos (segundos desde origen) en que se 
        #                 espera que la onda pase en cierta coordenada
        # onda_e        = Nombre de onda
        # ----------     
        
        #List to save values
        y_e_p = []
        x_e_p = []
        time_e = []
        onda_e = []
        
        #Loop para generar todos los puntos esperados
        for name,yv,xv,t,onda in zip(est['Est'],est['Lat'],est['Lon'],est['DeltaT (segundos)'],est['Onda']):
            #New point or expected point
            dx, dy = xv-xo, yv-yo
            var = 1
            #Generation of expected wave points
            while(var <= t):
                x_p = var*dx/t+xo
                y_p = var*dy/t+yo
                #Saving points
                x_e_p.append(x_p)
                y_e_p.append(y_p)
                time_e.append(var)
                onda_e.append(onda)
                #print("Expeted point ",var,": ",x_p,y_p)
                var= var+1
                
        return x_e_p, y_e_p, time_e, onda_e
    
    
    # Estaciones a plotear
    def station_check(ploted,actual_time,tipo_onda):
        #Puntos a plotear
        xp = []
        yp = []  
        #Verificamos que estación detecto el sismo
        for name,lat,lon,time,onda in zip(est['Est'],est['Lat'],est['Lon'],est['DeltaT (segundos)'],est['Onda']):
            if time<=actual_time:
                nameO=name+onda
                if(nameO in ploted):
                    pass
                else:
                    if(onda==tipo_onda):
                        x,y = m(lon,lat)
                        xp.append(x)
                        yp.append(y)
                        #Dato ya ploteado
                        ploted.append(nameO)
        return xp,yp
    
    # Ondsa a plotear
    def wave_check(actual_time,tipo_onda,x_e_p,y_e_p,time_e,onda_e):
        #Puntos a plotear
        xp = []
        yp = []  
        #Verificamos que estación detecto el sismo
        for x,y,time,onda in zip(x_e_p,y_e_p,time_e,onda_e):
            #Buscamos los puntos esperados en ese instante y que sea la onda
            #Deseada
            if (time==actual_time and onda == tipo_onda):
                xp.append(x)
                yp.append(y)
                        
        return xp,yp
        
    # animation function 
    def animate(i): 
        #Buscamos en que estaciones aparecen las ondas P
        xp,yp = station_check(ploted,i,'P')           
        #Actualización de plot              
        plot = ax.plot(xp,yp,'s',marker='^',color='r', markersize=10,markeredgecolor = 'k')
        
        #Buscamos en que estaciones aparecen las ondas S
        xp,yp = station_check(ploted,i,'S')           
        #Actualización de plot              
        plot = ax.plot(xp,yp,'s',marker='^',color='g', markersize=10,markeredgecolor = 'k')
        
        #Actualización de título
        plt.title('Segundos desde Origen: '+str(i))
        # return plot object 
        return plot
    
    # animation function 2
    def animate2(i): 
        x_pts,y_pts,t_pts,w_pts = expected_wave_points(float(data[1]),float(data[0]),est) 
        #Buscamos en que estaciones aparecen las ondas P
        xp , yp = wave_check(i,'P',x_pts,y_pts,t_pts,w_pts)
        #Actualización de plot              
        plot = ax.plot(xp,yp,'s',marker='.',color='r', markersize=2,markeredgecolor = 'k')
        
        #Buscamos en que estaciones aparecen las ondas S
        xp , yp = wave_check(i,'S',x_pts,y_pts,t_pts,w_pts)
        #Actualización de plot              
        plot = ax.plot(xp,yp,'s',marker='*',color='b', markersize=4,markeredgecolor = 'k')
        
        #Actualización de título
        plt.title('Segundos desde Origen: '+str(i))
        # return plot object 
        return plot
    
    #Variable de control
    ploted = []
    
    if(EXPECTED == False):
        # call the animator 
        anim = animation.FuncAnimation(fig, animate2, init_func=init, frames=t_max, interval=500)
        
    if(EXPECTED):
        # call the animator     
        anim = animation.FuncAnimation(fig, animate, init_func=init, frames=t_max, interval=500)
    
    #Decicimos guardar el vídeo 
    if(False):
        # save the animation as mp4 video file 
        writervideo = animation.FFMpegWriter(fps=2) 
        #Directoio de Pruebas
        if(homeDir == "C:/Users/HRV/Desktop/Post-U/Trabajo/Prueba/Data/Eventos/"):
            anim.save('Imagenes/'+str(folder)+'Prueba.mp4', writervideo )
        #Directorio en compu del trabajo
        else:
            anim.save(homeDir+str(folder)+'.mp4', writervideo )
    
    # save the animation as GIF file 
    # writergif = animation.PillowWriter(fps=10) 
    # anim.save('random.gif', writer=writergif)
    
#homeDir = "C:/Users/HRV/Desktop/Post-U/Trabajo/Prueba/Data/Eventos/"
#folder = '2019-11-13-1628'
#Animate_event(folder, homeDir,EXPECTED = False)