# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 23:23:45 2020

@author: Steven Rubio

Programa que buscar determinar que tan "triangulable" podría ser un evento en 
base a donde se encuentran las estaciones
"""

import matplotlib.pyplot as plt
import numpy as np

Est = [(2,1,6),(1,6,4)]

x = np.linspace(0.0, 10.0)
y = np.linspace(0.0, 10.0)

plt.plot(Est[0],Est[1], 'o')
plt.show()