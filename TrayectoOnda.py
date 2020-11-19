# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 04:43:13 2020

@author: HRV
"""
import matplotlib.pyplot as plt

yo, xo = -90.9997 , 13.7014
plt.plot(xo,yo,'ro')

#Random Event coordinates and arrival times
y = [ -89.8975 ,-90.4457 ,-90.4816 ,-90.5959 ,-90.7611 ,-90.3014 ,-89.9847 ,-90.4847]
x = [  14.2832 , 14.5447 , 14.5656 , 14.5993 , 14.3111 , 14.2791 , 14.6322 , 14.4787]
time = [20.69, 18.14, 9.6, 12.96, 16.63, 23.56, 16.50, 17.98]

#List to save values
y_e_p = []
x_e_p = []
time_e = []

#Loop for looking at the arrays
for xv,yv,t in zip(x,y,time):
    #Plot
    plt.plot(xv,yv,'bo')
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
        #print("Expeted point ",var,": ",x_p,y_p)
        plt.plot(x_p,y_p,'k^')
        var= var+1
  

plt.show()