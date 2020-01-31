#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 05:17:35 2020

@author: Steven
"""

#Vamos a editar la imagen con filtros
import cv2
from matplotlib import pyplot as plt
img = cv2.imread('ImagenPrueba.png')
blur = cv2.GaussianBlur(img,(5,5),0)

plt.imshow(blur),plt.xticks([]), plt.yticks([])
plt.savefig('Imagenes/ImagenPrueba_Filtrada.png', bbox_inches='tight')
plt.show()