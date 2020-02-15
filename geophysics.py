#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 17:17:05 2019

@author: Christian Ramirez
"""
import os
from obspy import read
import numpy as np
from datetime import datetime, date, timedelta
import math
#import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.colors as mcolors
import matplotlib.cm as cm

radioTierra = 6371
def color_list(lista):
    '''
    Resive una lista y devuelve colores
    '''
    a = max(lista)
    b = min(lista)
    norm = mpl.colors.Normalize(b, a)
    cmap = cm.jet
    mc = cm.ScalarMappable(norm = norm, cmap = cmap)
    color = []
    for i in range(len(lista)):
        a = mcolors.to_hex(mc.to_rgba(lista[i]))
        color.append(a)
    return color

def color_listf(lista,a,b):
    '''
    Resive una lista y devuelve colores
    '''
    norm = mpl.colors.Normalize(b, a)
    cmap = cm.jet
    mc = cm.ScalarMappable(norm = norm, cmap = cmap)
    color = []
    for i in range(len(lista)):
        a = mcolors.to_hex(mc.to_rgba(lista[i]))
        color.append(a)
    return color

def color_num(maximo,minimo,numero):
    '''
    Resive una numero y devuelve color
    '''
    norm = mpl.colors.Normalize(minimo, maximo)
    cmap = cm.jet
    mc = cm.ScalarMappable(norm = norm, cmap = cmap)
    a = mcolors.to_hex(mc.to_rgba(numero))
    return a

def int1(logpga):
    '''
    Esta funcion retorna el valor de la intensidad sismica de una estacion 
    como argumento exige el logaritmo del pga de cada estacion para condicion
    de tint 1
    '''
    return 2.270 + 1.647*(logpga)

def int2(logpga):
    '''
    Esta funcion retorna el valor de la intensidad sismica de una estacion 
    como argumento exige el logaritmo del pga de cada estacion para condicion
    de tint 2
    '''
    return -1.361 + 3.822*(logpga)

def ubicacion(nombre_estacion):
    """
    Esta funcion tiene como argumentos el numbre de las estaciones entre estos puden ser:
    CIRS, XELA, COBAN, entre otros (consultar trabla).
    
    Ejemplos:
    >>> ubicacion("CIRS")
    ('CIRS', '14.6568', '-90.5136')
    
    >>> ubicacion('COBAN')
    ('COBAN', '15.4716', '-90.3767')
    """
    #Se abre el archivo para lectura
    f=open('est.site', "r")
    if os.stat('est.site').st_size == 0:
        print('Archivo vacío.')
    else:
        tamaño_archivo = os.stat('est.site').st_size
        while tamaño_archivo != 0:
            linea = f.readline()
            lineas = linea.split()
            if not linea: 
                break  # Si no hay más se rompe bucle
            #print(lineas)  # Muestra la línea leída
            
            sigla = lineas[0]#busca en el archivo la longtud y latitud
            latitud = lineas[3]
            longitud = lineas[4]
            if nombre_estacion == sigla:
                #print("ESTACION: " + nombre_estacion)
                #print("Longitud: " + latitud) 
                #print("Latitud: " + longitud)
                return (nombre_estacion, latitud, longitud)
            f.close  # Cierra archivo'''
            
def todas_estaciones():
    '''
    Saca una lista todas las estaciones y se definidas mediante la clase estacion
    '''
    f=open('est.site', "r") #abre un archivo .site que debe ir junto a el
    estaciones = []
    if os.stat('est.site').st_size == 0:
        print('Archivo vacío.')
    else:
        tamaño_archivo = os.stat('est.site').st_size
        while tamaño_archivo != 0:
            linea = f.readline()
            lineas = linea.split()
            if not linea:
                break
            sigla = lineas[0]
            sigla = estacion(sigla)
            estaciones.append(sigla)
    return estaciones

def dia(fecha):
    '''
    Argumento de la funcion AAAA-MM-DD
    
    Calcula el numero del dia en el year
    '''
    year = int(fecha[:4]) #Cambia la variable de str a int
    mes = int(fecha[5:7])
    dia = int(fecha[8:10])
    fecha_inicial = datetime(year,1,1) #define fecha de inicio de la cuenta
    fecha = datetime(year,mes,dia) #convierte clase datetime la fecha
    a = date.toordinal(fecha) - date.toordinal(fecha_inicial) #hace la restay lo convierte a numero ordinal
    return str(a+1).zfill(3)

def diainv(cod, year):
    '''
    Como argumentos se necesita el numero de dia en el year y el year
    
    '''
    fecha_inicial = datetime(year,1,1) #define la fecha de inicio de la cuenta
    fecha = fecha_inicial + timedelta(days = cod-1) #coloca el contador en la feha deseada
    return str(fecha.year) + '-' + str(fecha.month).zfill(2) + '-' + str(fecha.day).zfill(2) #conviert de clase fecha a clase str

def epi_profundidad(namePath):
    '''
    Esta funcion retona lo ubicacion del epicentro del evento y la profundidad del mismo si estos no tienen 
    retorna la funcion vacia. Recibe como parametro el directorio donde se encuentra ubicado el archivo.
    
    '''    
    archivo = open(namePath,"r")
    palabra = []
    palabra2 = []
    longitud = 0.0
    latitud = 0.0
    profundidad = 0.0
    magnitud = 0.0
    
    for linea in archivo.readlines():
        palabra2 = linea.split(" ")
        for i in palabra2:
            if (i != ''):
                palabra.append(i)
                
        
        try:
            if (float(palabra[2])>0):
                longitud = float(palabra[0])
                latitud = palabra[1]
                profundidad = palabra[2]
                magnitud = palabra[20]
                break
        except:
            continue
        palabra = []
    archivo.close()
    return(longitud,latitud,profundidad,magnitud)
    
def distancia(lat1, long1, a):
        '''

        '''
        global radioTierra
        lat2 = a.epilat
        long2 = a.epilon
        #print(lat1,lat2,long1,long2)
        
    
        difLat = np.radians(lat2 - lat1) #Δlat en radianes
        difLong = np.radians(long2 - long1) #Δlong en radianes
        
        a1 = pow(np.sin(difLat/2),2)    #sin²(Δlat/2)
        a2 = np.cos(np.radians(lat1))     #cos(lat1) donde lat1 esta en radianes
        a3 = np.cos(np.radians(lat2))     #cos(lat2) donde lat2 esta en radianes
        a4 = pow(np.sin(difLong/2),2)   #sin²(Δlong/2)
        a = a1 + a2 * a3 * a4
    
        c = 2 * np.arctan2(np.sqrt(a),np.sqrt(1-a)) #2 · atan2(√a, √(1−a))
    
        d = radioTierra * c
        
        return d
def distancia2(lat1, long1, lat2, long2):
        '''

        '''
        global radioTierra
        #print(lat1,lat2,long1,long2)
        
    
        difLat = np.radians(lat2 - lat1) #Δlat en radianes
        difLong = np.radians(long2 - long1) #Δlong en radianes
        
        a1 = pow(np.sin(difLat/2),2)    #sin²(Δlat/2)
        a2 = np.cos(np.radians(lat1))     #cos(lat1) donde lat1 esta en radianes
        a3 = np.cos(np.radians(lat2))     #cos(lat2) donde lat2 esta en radianes
        a4 = pow(np.sin(difLong/2),2)   #sin²(Δlong/2)
        a = a1 + a2 * a3 * a4
    
        c = 2 * np.arctan2(np.sqrt(a),np.sqrt(1-a)) #2 · atan2(√a, √(1−a))
    
        d = radioTierra * c
        
        return d

class evento:
    """
    La clase evento representa atributos de los eventos sismográficos detectados 
    por Instituto de Investigaciones de Ingenieria, Matematica 
    y Ciencias Fisicas de la Universidad Dr. Mariano Galvez de Guatemala.
    
    Estos administrados por el software Antelope y el programa busca entre las carpetas del mismo
    siempre y cuando se preserve el formato
    """
    def __init__(self, nombre):
        self.codigo = nombre
        self.year = nombre[0:4]
        self.mes = nombre[5:7]
        self.dia = str(dia(nombre))
        self.path = self.year + '/' + self.mes + '/' + self.codigo
        self.incod = self.year + self.dia + nombre[11:15]
        self.regis = self.path + '/' + self.year + '/' + self.dia
        try:
            self.epilon = float(epi_profundidad(self.path + '/' + self.incod + '.origin')[1]) #returnPath(nombre + '.origin')
        except:
            self.epilon = (epi_profundidad(self.path + '/' + self.incod + '.origin')[1])  #fichero_evento
        try:
            self.epilat = float(epi_profundidad(self.path + '/' + self.incod + '.origin')[0])
        except:
            self.epilat = (epi_profundidad(self.path + '/' + self.incod + '.origin')[0])
        try:
            self.prof = float(epi_profundidad(self.path + '/' + self.incod + '.origin')[2])
        except:
            self.prof = (epi_profundidad(self.path + '/' + self.incod + '.origin')[2])
        try:
            self.mag = float(epi_profundidad(self.path + '/' + self.incod + '.origin')[3])
        except:
            self.mag = (epi_profundidad(self.path + '/' + self.incod + '.origin')[3])
    
    def aceleraciones(self, sta):
        '''
        Función realiza el cálculo las aceleraciones obtenidas del archivo 
        indicado por el argumento sta.
        sta es el nombre de la estación del cual se desea obtener 
        las aceleraciones.
        '''
        
        directorio = self.regis
        
        listadearchivos = sorted(os.listdir(directorio))
        E = []
        N = []
        Z = []
        for i in listadearchivos:
            frase = []
            palabra = ""
            for j in i:
                if j == ".":
                    frase.append(palabra)
                    palabra = ''
                else:
                    palabra += j
                if palabra == sta:
                    directorio = directorio + "/" +  i
                    a = read(directorio)
                    tl = a[0]
                    if len(E) < 1:
                        E = tl.data
                    elif len(N) < 1:
                        N = tl.data
                    elif len(Z) < 1:
                        Z = tl.data
                    else:
                        pass
                else:
                    pass
            directorio = self.regis

            AE = []
            AN = []
            AZ = []
            for i in E:
                a = i * 2365.26
                AE.append(a)
            for i in N:
                a = i * 2365.26
                AN.append(a)
            for i in Z:
                a = i * 2365.26
                AZ.append(a)
        return [AE,AN,AZ]
    def pga(self,i):
        '''
        Función que indica el pga de una estación. El resultado es una tupla
        almacenada en una lista, con la información calculada del pga.
        
        Recibe como parámetro a:
            i = string que contiene la información y propiedades de la estación.
        '''        
        pga_por_estacion = []
        try:
            a = self.aceleraciones(i)
            gal = ((max(abs(max(a[0])),abs(max(a[1])),abs(max(a[2])),abs(min(a[0])),abs(min(a[1])),abs(min(a[2])))-abs(max(np.mean(a[0]),np.mean(a[1]),np.mean(a[2]))))/pow(10,7))
            ampl = (gal)/9.81
            pga_por_estacion.append((i, gal, ampl)) # 1 es gal 2 es porcentaje de g
        except Exception as e:
            print(e)
        return pga_por_estacion
    

    def pgalist(self):
        '''
        Listas de pga para cada estacion que este en funcionamiento durante el evento
        tomar en cuenta que en algunas estaciones lejanas no es detectado
        '''
        a = todas_estaciones()
        pa = []
        for i in a:
            print(i.name)
            try:
                x = self.pga(i.name)
                if len(x) != 0:
                    pa.append(x)
                else:
                    pass
            except:
                pass
        print('pga calculado')
        return pa
    
    def intensidad(self):
        '''
        Listas de intensidad para cada estacion que este en funcionamiento durante el evento
        tomar en cuenta que en algunas estaciones lejanas no es detectado
        '''
        tint = 4.87
        p = self.pgalist()
        for i in p:
            print(i[0][0] + 'check')
            try:
                if np.log(abs(i[0][2])) < tint or np.log(abs(i[0][2])) == tint:
                    i[0] = list(i[0])
                    i[0].append(int1(np.log10(abs(i[0][2]))))
                else:
                    i[0] = list(i[0])
                    i[0].append(int2(np.log10(abs(i[0][2]))))
            except:
                pass
            
        print('intensidad calculada')
        return p
        
        
        




class estacion:
    '''
    La clase estacion fue definida para facilitar el manejo de la informacion
    esta clase representa a las estaciones que existen dentro de la red 
    aceklerografica del Instituto de Investigaciones de Ingenieria, Matematica 
    y Ciencias Fisicas de la Universidad Dr. Mariano Galvez de Guatemala
    '''
    def __init__(self, nombre):
        '''
        La clase estacion tiene tres caracteristicas principales, nombre,
        latitud y longitud para acceder a ellas se debe poner lo siguiente
        
        sea self el nombre o la variable asociada
        
        self.name nombre de la estacion tipo cadena
        self.longitud la coordenada de longitud en la ubicacion de la estacion 
        tipo flotante
        self.latitud la coordenada de latitud en la ubicacion de la estacion 
        tipo flotante
        
        '''
        self.name = nombre
        self.longitud = float(ubicacion(nombre)[2])
        self.latitud = float(ubicacion(nombre)[1])
    
    
    def __repr__(self):
       return 'Nombre: {} Ubicada en Latitud = {} y Longitud = {}'.format(self.name, self.latitud, self.longitud)
    
    def __str__(self):
        return 'Nombre: {} Ubicada en Latitud = {} y Longitud = {}'.format(self.name, self.latitud, self.longitud)
    
    def depicentro(self, a):
        '''
        El metodo depicentro requiere dos argumentos self que es la estacion
        y a que es una varable local tipo evento (buscar help(evento) para mas 
        informacion) 
        
        Este metodo calcula la distancia epicentral de la estacion escogida al epicentro
        del evento seleccionado
        '''
        global radioTierra
        lat1 = self.latitud
        lat2 = a.epilat
        long1 = self.longitud
        long2 = a.epilon
        
    
        difLat = math.radians(lat2 - lat1) #Δlat en radianes
        difLong = math.radians(long2 - long1) #Δlong en radianes
        
        a1 = pow(math.sin(difLat/2),2)    #sin²(Δlat/2)
        a2 = math.cos(math.radians(lat1))     #cos(lat1) donde lat1 esta en radianes
        a3 = math.cos(math.radians(lat2))     #cos(lat2) donde lat2 esta en radianes
        a4 = pow(math.sin(difLong/2),2)   #sin²(Δlong/2)
        a = a1 + a2 * a3 * a4
    
        c = 2 * math.atan2(math.sqrt(a),math.sqrt(1-a)) #2 · atan2(√a, √(1−a))
    
        d = radioTierra * c
        print(d)
        return d
    
