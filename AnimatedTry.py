# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 02:48:57 2020

@author: Hiram

Aprendiendo a hacer imagenes animadas
"""


import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation
import matplotlib.pyplot as plt

from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import random

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


#Data Aleatoria
x = [random.randint(61000,500000) for i in range(100)]
y = [random.randint(61000,500000) for i in range(100)]

# initialization function 
def init(): 
    # plot the first day (day=0) here:
    plot = ax.plot(x[0],y[0])
    return plot

# animation function 
def animate(i): 
    plot = ax.plot(x[i],y[i],marker='*',markersize=7)
    # return plot object 
    return plot

# call the animator     
anim = animation.FuncAnimation(fig, animate, init_func=init, frames=99, interval=200,save_count=2000)
#plt.show()

# save the animation as mp4 video file 
writervideo = animation.FFMpegWriter(fps=10) 
anim.save('Imagenes/random.mp4', writervideo )

# save the animation as GIF file 
# writergif = animation.PillowWriter(fps=10) 
# anim.save('random.gif', writer=writergif)
