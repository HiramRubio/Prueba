
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 12:03:01 2019

@author: Steven Rubio
"""

import matplotlib.pyplot as plt
import pyproj as proj
import numpy as np; np.random.seed(1)
from scipy.spatial import ConvexHull

crs_wgs = proj.Proj(init='epsg:4326')  # assuming you're using WGS84 geographic

#Erect own local flat cartesian coordinate system
#Colocamos el punto central de nuestro sistema
#En ese caso escogi la UMG
gps_lat_0 = 14.656501
gps_long_0 = -90.512975
cust = proj.Proj("+proj=aeqd +lat_0={0} +lon_0={1} +datum=WGS84 +units=m".format(gps_lat_0, gps_long_0))
#x, y = proj.transform(crs_wgs, cust, gps_long, gps_lat)

#Array para almacenar puntos mapeados
P = []

#Estaciones
SMARC 	= 	(14.9580,  -91.8023)
PSMARC = proj.transform(crs_wgs, cust,	SMARC[1],SMARC[0])
P.append(('SMARC',PSMARC[0],PSMARC[1],2.07983275882))

HUEH  	=  	(15.3162,  -91.4851)
PHUEH = proj.transform(crs_wgs, cust, 	HUEH[1],HUEH[0])
P.append(('HUEH',PHUEH[0],PHUEH[1],1.10527256868))

VILL    = 	(14.5041,  -90.6131) 
PVILL= proj.transform(crs_wgs, cust,	VILL[1],VILL[0])
P.append(('VILL',PVILL[0],PVILL[1],4.12224015391))

XELA    = 	(14.8618,  -91.5491)
PXELA = proj.transform(crs_wgs, cust,	XELA[1],XELA[0])
P.append(('XELA',PXELA[0],PXELA[1],0.879594584205))

JUTI  	=	(14.2832,  -89.8975 )
PJUTI= proj.transform(crs_wgs, cust, 	JUTI[1], JUTI[0])
P.append(('JUTI',PJUTI[0],PJUTI[1],0.809678135629))

CIRS    =  	(14.6568,  -90.5136 )
PCIRS= proj.transform(crs_wgs, cust, CIRS[1], CIRS[0])
#P.append(('CIRS',PCIRS[0],PCIRS[1]))

ANTG   	=   (14.5600,  -90.7352 )
PANTG= proj.transform(crs_wgs, cust, ANTG[1], ANTG[0])
P.append(('ANTG',PANTG[0],PANTG[1],3.58528591905))

SJPIN   =   (14.5447,  -90.4457 )
PSJPIN= proj.transform(crs_wgs, cust, SJPIN[1], SJPIN[0])
P.append(('SJPIN',PSJPIN[0],PSJPIN[1],3.36580599722))

CMONM  	=   (14.5834,  -90.5632)
PCMONM= proj.transform(crs_wgs, cust, CMONM[1], CMONM[0])
#P.append(('CMONM',PCMONM[0],PCMONM[1]))

CINGE   =   (14.6121,  -90.5311)
PCINGE= proj.transform(crs_wgs, cust, CINGE[1], CINGE[0])
#P.append(('CINGE',PCINGE[0],PCINGE[1]))

CSTER   =   (14.6035,  -90.5568 )
PCSTER= proj.transform(crs_wgs, cust, CSTER[1], CSTER[0])
P.append(('CSTER',PCSTER[0],PCSTER[1],3.34070480035))

KINAL   =   (14.6255,  -90.5357)
PKINAL= proj.transform(crs_wgs, cust, KINAL[1], KINAL[0])
#P.append(('KINAL',PKINAL[0],PKINAL[1]))

CASUN   =   (14.6012,  -90.5076)
PCASUN= proj.transform(crs_wgs, cust, CASUN[1], CASUN[0])
#P.append(('CASUN',PCASUN[0],PCASUN[1]))

ITC     =   (14.6458,  -90.5063 )
PITC= proj.transform(crs_wgs, cust, ITC[1], ITC[0])
P.append(('ITC',PITC[0],PITC[1],2.94606409247))

EXCEL   =   (14.5803,  -90.4940)
PEXCEL= proj.transform(crs_wgs, cust, EXCEL[1], EXCEL[0])
P.append(('EXCEL',PEXCEL[0],PEXCEL[1],2.7476506825))

CCONS   =   (14.5656,  -90.4816)
PCCONS= proj.transform(crs_wgs, cust, CCONS[1], CCONS[0])
P.append(('CCONS',PCCONS[0],PCCONS[1],2.26575082403))

IPRES   =   (14.6436,  -90.5127)
PIPRES= proj.transform(crs_wgs, cust, IPRES[1], IPRES[0])
#P.append(('IPRES',PIPRES[0],PIPRES[1]))

TADEO   =   (14.5854,  -90.5193)
PTADEO= proj.transform(crs_wgs, cust, TADEO[1], TADEO[0])
#P.append(('TADEO',PTADEO[0],PTADEO[1]))

CBIBL   =   (14.5923,  -90.5497 )
PCBIBL= proj.transform(crs_wgs, cust, CBIBL[1], CBIBL[0])
#P.append(('CBIBL',PCBIBL[0],PCBIBL[1]))

CAUST   =   (14.6213,  -90.4852 )
PCAUST= proj.transform(crs_wgs, cust, CAUST[1], CAUST[0])
P.append(('CAUST',PCAUST[0],PCAUST[1],2.69701983303))

LSECB   =   (14.6080,  -90.6052)
PLSECB= proj.transform(crs_wgs, cust, LSECB[1], LSECB[0])
P.append(('LSECB',PLSECB[0],PLSECB[1],3.85884363093))

SEUNI   =   (14.6109,  -90.5160 )
PSEUNI= proj.transform(crs_wgs, cust, SEUNI[1], SEUNI[0])
#P.append(('SEUNI',PSEUNI[0],PSEUNI[1],3.24770459239))

JUAMA   =   (14.5714,  -90.5286 )
PJUAMA= proj.transform(crs_wgs, cust, JUAMA[1], JUAMA[0])
P.append(('JUAMA',PJUAMA[0],PJUAMA[1],2.82305071441))

SETEC   =   (14.6212,  -90.5268 )
PSETEC= proj.transform(crs_wgs, cust, SETEC[1], SETEC[0])
#P.append(('SETEC',PSETEC[0],PSETEC[1]))

ACRIS   =   (14.5993,  -90.5959 )
PACRIS= proj.transform(crs_wgs, cust, ACRIS[1], ACRIS[0])
P.append(('ACRIS',PACRIS[0],PACRIS[1],3.40107761673))

ASEGG   =   (14.6038,  -90.5128  )
PASEGG= proj.transform(crs_wgs, cust, ASEGG[1], ASEGG[0])
#P.append(('ASEGG',PASEGG[0],PASEGG[1]))

CDBOS   =   (14.6241,  -90.5207)
PCDBOS= proj.transform(crs_wgs, cust, CDBOS[1], CDBOS[0])
P.append(('CDBOS',PCDBOS[0],PCDBOS[1],2.83860456664))

RGIL    =   (14.5841,  -90.4879)
PRGIL= proj.transform(crs_wgs, cust, RGIL[1], RGIL[0])
P.append(('RGIL',PRGIL[0],PRGIL[1],2.39857050911))

COBAN   =   (15.4716,  -90.3767 )
PCOBAN= proj.transform(crs_wgs, cust, COBAN[1], COBAN[0])
P.append(('COBAN',PCOBAN[0],PCOBAN[1],1.67823449724))

AMGGT   =   (14.6314,  -90.5388)
PAMGGT= proj.transform(crs_wgs, cust, AMGGT[1], AMGGT[0])
#P.append(('AMGGT',PAMGGT[0],PAMGGT[1]))

CHAMP   =   (14.2946,  -91.9140)
PCHAMP= proj.transform(crs_wgs, cust, CHAMP[1], CHAMP[0])
P.append(('CHAMP',PCHAMP[0],PCHAMP[1],0.721837741498))

JUNKA   =   (14.6204,  -90.5293)
PJUNKA= proj.transform(crs_wgs, cust, JUNKA[1], JUNKA[0])
#P.append(('JUNKA',PJUNKA[0],PJUNKA[1]))

IZABA   =   (15.7472,  -88.5780 )
PIZABA= proj.transform(crs_wgs, cust, IZABA[1], IZABA[0])
P.append(('IZABA',PIZABA[0],PIZABA[1],1.13014912141))

SALAM   =   (15.1010,  -90.3179 )
PSALAM= proj.transform(crs_wgs, cust, SALAM[1], SALAM[0])
P.append(('SALAM',PSALAM[0],PSALAM[1],2.20230331993))

CHULA   =   (13.9160,  -90.8911 )
PCHULA= proj.transform(crs_wgs, cust, CHULA[1], CHULA[0])
#P.append(('CHULA',PCHULA[0],PCHULA[1]))

ZACAP   =   (14.9716,  -89.5417 )
PZACAP= proj.transform(crs_wgs, cust, ZACAP[1], ZACAP[0])
#P.append(('ZACAP',PZACAP[0],PZACAP[1]))

QUICH   =   (15.0295,  -91.1445 )
PQUICH= proj.transform(crs_wgs, cust, QUICH[1], QUICH[0])
#P.append(('QUICH',PQUICH[0],PQUICH[1]))

ESCTL  =    (14.3111,  -90.7611 )
PESCTL= proj.transform(crs_wgs, cust, ESCTL[1], ESCTL[0])
#P.append(('ESCTL',PESCTL[0],PESCTL[1]))

CEPRO   =   (14.6651,  -90.4942 )
PCEPRO= proj.transform(crs_wgs, cust, CEPRO[1], CEPRO[0])
#P.append(('CEPRO',PCEPRO[0],PCEPRO[1]))
"""
STARS   =   (14.2791,  -90.3014 )
PSTARS= proj.transform(crs_wgs, cust, STARS[1], STARS[0])
P.append(('STARS',PSTARS[0],PSTARS[1]))

LGUAT   =   (14.6160,  -90.5133 )
PLGUAT= proj.transform(crs_wgs, cust, LGUAT[1], LGUAT[0])
P.append(('LGUAT',PLGUAT[0],PLGUAT[1]))

SMP    =    (14.5200,  -90.5556  )
PSMP= proj.transform(crs_wgs, cust, SMP[1], SMP[0])
P.append(('SMP',PSMP[0],PSMP[1]))

CSAGC  =    (14.6221,  -90.4724  )
PCSAGC= proj.transform(crs_wgs, cust, CSAGC[1], CSAGC[0])
P.append(('CSAGC',PCSAGC[0],PCSAGC[1]))

SPAYM   =   (14.6875,  -90.4594 )
PSPAYM= proj.transform(crs_wgs, cust, SPAYM[1], SPAYM[0])
P.append(('SPAYM',PSPAYM[0],PSPAYM[1]))

JALAP  =    (14.6322,  -89.9847 )
PJALAP	= proj.transform(crs_wgs, cust, JALAP[1], JALAP[0])
P.append(('JALAP',PJALAP[0],PJALAP[1]))

BVH     =  	(14.4787,  -90.4847)  
PBVH= proj.transform(crs_wgs, cust, BVH[1], BVH[0])
P.append(('BVH',PBVH[0],PBVH[1]))
"""

EPI     =  	(14.4469,  -90.6948)  
PEPI= proj.transform(crs_wgs, cust, EPI[1], EPI[0])
P.append(('EPI',PEPI[0],PEPI[1],3.1901278218733635))
         
#Definimos nuestra region
xo, yb1 = proj.transform(crs_wgs, cust, -93.311536, 15.011392)
xf, yb2 = proj.transform(crs_wgs, cust, -87.982886, 14.723266)
xb1, yo = proj.transform(crs_wgs, cust, -90.504369, 13.361663)
xb2, yf = proj.transform(crs_wgs, cust, -90.305631, 16.219592)
Dx = (xo,xf)
Dy = (yo,yf)

C1 = []
C2 = []
C3 = []
for i in range(0,len(P)):
    C1.append(P[i][1])
    C2.append(P[i][2])
    C3.append(P[i][3])

plt.plot(C1,C2, 'ro',PEPI[0],PEPI[1],'go')
#------------------------------------------

#Encerrando la data con poligonos irregulares
def encircle(x,y, ax=None, **kw):
    if not ax: ax=plt.gca()
    p = np.c_[x,y]
    hull = ConvexHull(p)
    poly = plt.Polygon(p[hull.vertices,:], **kw)
    ax.add_patch(poly)

#Encerrando la data con un elipsoide
def encircle2(x,y, ax=None, **kw):
    if not ax: ax=plt.gca()
    p = np.c_[x,y]
    mean = np.mean(p, axis=0)
    d = p-mean
    r = np.max(np.sqrt(d[:,0]**2+d[:,1]**2 ))
    circ = plt.Circle(mean, radius=1.05*r,**kw)
    ax.add_patch(circ)

#Defino 4 regiones
h = (max(C3)-min(C3))/5
R1x = []
R1y = []
R2x = []
R2y = []
R3x = []
R3y = []
R4x = []
R4y = []
R5x = []
R5y = []
for i in range(0,len(P)):
    if C3[i]> (min(C3)):
        R1x.append(C1[i])
        R1y.append(C2[i])
        if C3[i]> (min(C3)+h):
            R2x.append(C1[i])
            R2y.append(C2[i])
            if C3[i]> (min(C3)+2*h):
                R3x.append(C1[i])
                R3y.append(C2[i])
                if C3[i]> (min(C3)+3*h):
                    R4x.append(C1[i])
                    R4y.append(C2[i])
                    if C3[i]> (min(C3)+4*h):
                        R5x.append(C1[i])
                        R5y.append(C2[i])

encircle(R1x, R1y, ec="blue", fc="none", alpha=0.2)
encircle(R2x, R2y, ec="green", fc="none", alpha=0.2)
encircle(R3x, R3y, ec="yellow", fc="none", alpha=0.2)
encircle(R4x, R4y, ec="orange", fc="none", alpha=0.2)
encircle(R5x, R5y, ec="red", fc="gold", alpha=0.2)
plt.gca().relim()
plt.gca().autoscale_view()
plt.show()
    
