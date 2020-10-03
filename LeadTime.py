# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 02:43:17 2020

@author: Steven Hiram
"""

def Estacion_Capital(Estat):
    val = False
    CIUDAD = ['CIRS','VILL','SJPIN','CMONM','CINGE','CSTER','CASUN','KINAL',
              'ITC','JUAMA','EXCEL','CCONS','IPRES','TADEO','CBIL','CAUST',
              'LSECB','ICREY','ACRIS','SEUNI','ASEGG','CSAGC','AMGGT','LGUAT',
              'CDBOS','RGIL','JUNKA','CEPRO','NRNJO','SMP','SPAYM','BVH','ALUX',
              'TUC','VILLC','MERCK','RCACE']
    if(Estat in CIUDAD):   val = True
    return val
