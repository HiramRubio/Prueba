#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 10:34:59 2020

@author: rt
"""

import numpy as np



def Intensidad_E(Ex,Ey,Px,Py,Esx,Esy,IE,IP):
    """
    Ex, Ey = Puntos x,y del Epicentro
    Px, Py = Puntos x,y del punto que se va a estimar
    Esx, Esy = Puntos x,y de la Estacion
    IE = Intensidad Epicentro
    IP = Intensidad Punto
    """
    a = np.array([Ex,Ey])
    b = np.array([Px,Py])
    c = np.array([Esx,Esy])

    ba = a - b
    bc = c - b
    #Distancia Epicentro
    d_ba = np.linalg.norm(ba) 
    #Distancia Punto
    d_bc = np.linalg.norm(bc)

    cosine_angle = np.dot(ba, bc) / (d_ba * d_bc)
    angle = np.arccos(cosine_angle)
    angle_d = np.degrees(angle)
    print(angle_d)
    if (angle_d>80.0 and angle_d<100.0):
        I_est = IE - (d_ba/ (d_ba+d_bc) )*IP
    else: I_est = 0
    return(I_est,angle_d)
    
x,y = Intensidad_E(6,0,0,0,0,6,10,5)
print(x)
x,y = Intensidad_E(1,0,0,0,0,6,10,5)
print(x)
x,y = Intensidad_E(6,0,0,0,0,1,10,5)
print(x)