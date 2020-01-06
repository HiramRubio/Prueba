#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 10:01:18 2019

@author: Sty
"""
import math
import portolan

def calculate_initial_compass_bearing(pointA, pointB):
    """
    Calculates the bearing between two points.
    The formulae used is the following:
        θ = atan2(sin(Δlong).cos(lat2),
                  cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))
    :Parameters:
      - `pointA: The tuple representing the latitude/longitude for the
        first point. Latitude and longitude must be in decimal degrees
      - `pointB: The tuple representing the latitude/longitude for the
        second point. Latitude and longitude must be in decimal degrees
    :Returns:
      The bearing in degrees
    :Returns Type:
      float
    """
    if (type(pointA) != tuple) or (type(pointB) != tuple):
        raise TypeError("Only tuples are supported as arguments")

    lat1 = math.radians(pointA[0])
    lat2 = math.radians(pointB[0])

    diffLong = math.radians(pointB[1] - pointA[1])

    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
            * math.cos(lat2) * math.cos(diffLong))

    initial_bearing = math.atan2(x, y)

    # Now we have the initial bearing but math.atan2 return values
    # from -180° to + 180° which is not what we want for a compass bearing
    # The solution is to normalize the initial bearing as shown below
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360
    #Aqui modifico el programa para que traducir el angulo a la nomencaltura
    #de compass con 16 divisiones. Llamo a la funcion que lo hace. 
    compass_range = compass_loc(compass_bearing)
    return compass_range

def compass_loc(degree): 
    #Calculo el cuadrante en el que me encuentro de los 16 posibles
    x = int(((degree + 11.25) % 360) / 22.5)
    #Casos
    if x==0: loc =str( "N")
    elif x==1: loc =str( "NNE")
    elif x==2: loc =str( "NE")
    elif x==3: loc =str( "ENE")
    #-----------------------#
    elif x==4: loc =str( "E")
    elif x==5: loc =str( "ESE")
    elif x==6: loc =str( "SE")
    elif x==7: loc =str( "SSE")
     #-----------------------#    
    elif x==8: loc =str( "S")
    elif x==9: loc =str( "SSO")
    elif x==10: loc =str( "SO")
    elif x==11: loc =str( "OSO")
    #-----------------------#
    elif x==12: loc =str( "O")
    elif x==13: loc =str( "ONO")
    elif x==14: loc =str( "NO")
    elif x==15: loc =str( "NNO") 
    #-----------------------#                          
    return loc
#Unos puntos para probar el metodo
p1 = (47.5606,-52.743099);
p2 = (47.594719,-52.685001);
p3 = (13.5235,-90.7281);
print ("Ready")

prueba = calculate_initial_compass_bearing(p1,p2);
prueba2 = calculate_initial_compass_bearing(p1,p3);
print(prueba)
print("--------------------------")
print(prueba2)
