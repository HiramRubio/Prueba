# -*- coding: utf-8 -*-
"""
Created on Thu May 21 04:57:47 2020

@author: HRV
"""


import matplotlib.pyplot as plt

coord = [[155354.419321672, 89815.9372730539], [208482.788011190, 268332.417436816], [172664.418413452, 240486.696751195]]
coord.append(coord[0]) #repeat the first point to create a 'closed loop'

xs, ys = zip(*coord) #create lists of x and y values

plt.figure()
plt.plot(xs,ys) 
plt.plot(155354.41932167154, 89815.9372730538,"ro")
plt.show() # if you need...