# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 02:48:57 2020

@author: Hiram

Aprendiendo a hacer imagenes animadas
"""


import pandas as pd
import matplotlib.pyplot as plt
#from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation
from mpl_toolkits.basemap import Basemap
import math
from stations_extractor import event_info_extractor

#Inicio de plot
fig, ax = plt.subplots(figsize=(8,8))
#Nacional
m = Basemap(resolution='i', # c, l, i, h, f or None
    lat_0=14.6569, lon_0=-90.51,
    llcrnrlon=-92.93, llcrnrlat=13.15,urcrnrlon=-87.58, urcrnrlat=18.42,
    projection='tmerc')
    
m.drawmapboundary(fill_color='#46bcec')                  
m.fillcontinents(color='#f2f2f2',lake_color='#46bcec')
#Leemos nuestra shapefile, no los activamos todos
m.readshapefile('Data/gtm/gtm_admbnda_adm0_ocha_conred_20190207', 'ej0',linewidth=1.5)
m.readshapefile('Data/gtm/gtm_admbnda_adm1_ocha_conred_20190207', 'ej1',linewidth=0.5)

#Data de cada estacion 
#Evento 2019-11-13-1628
est = pd.read_csv('Data/g1.csv',sep=';',names=['num1','Folder','Prof','mag','Est','Lat','Lon','Dist','Angle','Onda','DeltaT'])
#Directorio con data del evento
homeDir = "C:/Users/HRV/Desktop/Post-U/Trabajo/Prueba/Data/Eventos/"
#Data principal del evento
data = event_info_extractor('2019-11-13-1628',homeDir)

#Tiempo máximo
t_max =math.ceil(max(est['DeltaT']))+2
      
# initialization function 
def init(): 
    #Texto/Leyenda
    ax.plot(420000,400000,'s',marker='^',color='r', markersize=6)
    ax.plot(420000,410000,'s',marker='^',color='g', markersize=6)
    ax.text(430000,395000,'Onda P', fontsize=8)
    ax.text(430000,405000,'Onda S', fontsize=8)
    #Plot epicentro
    x,y = m(float(data[1]),float(data[0]))
    plot = ax.plot(x,y,'s',marker='*',color='k', markersize=10)
    return plot

# Estaciones a plotear
def station_check(ploted,actual_time,tipo_onda):
    #Puntos a plotear
    xp = []
    yp = []  
    #Verificamos que estación detecto el sismo
    for name,lat,lon,time,onda in zip(est['Est'],est['Lat'],est['Lon'],est['DeltaT'],est['Onda']):
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
    
# animation function 
def animate(i): 
    #Buscamos en que estaciones aparecen las ondas P
    xp,yp = station_check(ploted,i,'P')           
    #Actualización de plot              
    plot = ax.plot(xp,yp,'s',marker='^',color='r', markersize=10)
    
    #Buscamos en que estaciones aparecen las ondas S
    xp,yp = station_check(ploted,i,'S')           
    #Actualización de plot              
    plot = ax.plot(xp,yp,'s',marker='^',color='g', markersize=6)
    
    #Actualización de título
    plt.title('Segundos desde Origen: '+str(i))
    # return plot object 
    return plot

#Variable de control
ploted = []
# call the animator     
anim = animation.FuncAnimation(fig, animate, init_func=init, frames=t_max, interval=500)
plt.show()

# save the animation as mp4 video file 
writervideo = animation.FFMpegWriter(fps=2) 
anim.save('Imagenes/eventG1.mp4', writervideo )

# save the animation as GIF file 
# writergif = animation.PillowWriter(fps=10) 
# anim.save('random.gif', writer=writergif)
