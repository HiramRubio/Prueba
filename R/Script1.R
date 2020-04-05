data <- read.csv("C:/Users/HRV/Desktop/Post-U/Scripts/Prueba/Data/Anual2019_M.csv")
Zona0 <- data[ which (data$Zona==0),]
Zona1 <- data[ which (data$Zona==1),]
Zona2 <- data[ which (data$Zona==2),]
Zona3 <- data[ which (data$Zona==3),]
Zona4 <- data[ which (data$Zona==4),]
Zona5 <- data[ which (data$Zona==5),]
Zona6 <- data[ which (data$Zona==6),]
Zona7 <- data[ which (data$Zona==7),]
Zona8 <- data[ which (data$Zona==8),]

#-----------Zona 0----------------
jpeg('HZ0_M.jpg')
hist(Zona0$ml,main="Histograma magnitud sismos Zona SMG 0", 
xlab = "Magnitud (ml)",
ylab = "Frecuencia",
col="darkgreen")
dev.off()
#-----------------------------
jpeg('HZ0_P.jpg')
hist(Zona0$prof,main="Histograma profundidad sismos Zona SMG 0", 
xlab = "Profundidad (km)",
ylab = "Frecuencia",
col="gold",
seq(0,150, 25))
dev.off()
#--------------------------------
jpeg('HZ0_F.jpg')
hist(strtoi(Zona0$time),main="Histograma frecuencia sismos Zona SMG 0", 
xlab = "Día del año",
ylab = "Frecuencia",
col="blue",
seq(0,380,15))
dev.off()
#-----------Zona 1----------------
jpeg('HZ1_M.jpg')
hist(Zona1$ml,main="Histograma magnitud sismos Zona SMG 1", 
xlab = "Magnitud (ml)",
ylab = "Frecuencia",
col="darkgreen")
dev.off()
#-----------------------------
jpeg('HZ1_P.jpg')
hist(Zona1$prof,main="Histograma profundidad sismos Zona SMG 1", 
xlab = "Profundidad (km)",
ylab = "Frecuencia",
col="gold",
seq(0,150, 25))
dev.off()
#--------------------------------
jpeg('HZ1_F.jpg')
hist(strtoi(Zona1$time),main="Histograma frecuencia sismos Zona SMG 1", 
xlab = "Día del año",
ylab = "Frecuencia",
col="blue",
seq(0,380,15))
dev.off()
#-----------Zona 2----------------
jpeg('HZ2_M.jpg')
hist(Zona2$ml,main="Histograma magnitud sismos Zona SMG 2", 
xlab = "Magnitud (ml)",
ylab = "Frecuencia",
col="darkgreen")
dev.off()
#-----------------------------
jpeg('HZ2_P.jpg')
hist(Zona2$prof,main="Histograma profundidad sismos Zona SMG 2", 
xlab = "Profundidad (km)",
ylab = "Frecuencia",
col="gold",
seq(0,150, 25))
dev.off()
#--------------------------------
jpeg('HZ2_F.jpg')
hist(strtoi(Zona2$time),main="Histograma frecuencia sismos Zona SMG 2", 
xlab = "Día del año",
ylab = "Frecuencia",
col="blue",
seq(0,380,15))
dev.off()
#-----------Zona 3----------------
jpeg('HZ3_M.jpg')
hist(Zona3$ml,main="Histograma magnitud sismos Zona SMG 3", 
xlab = "Magnitud (ml)",
ylab = "Frecuencia",
col="darkgreen",
seq(2,5,0.25))
dev.off()
#-----------------------------
jpeg('HZ3_P.jpg')
hist(Zona3$prof,main="Histograma profundidad sismos Zona SMG 3", 
xlab = "Profundidad (km)",
ylab = "Frecuencia",
col="gold",
seq(0,200, 25))
dev.off()
#--------------------------------
jpeg('HZ3_F.jpg')
hist(strtoi(Zona3$time),main="Histograma frecuencia sismos Zona SMG 3", 
xlab = "Día del año",
ylab = "Frecuencia",
col="blue",
seq(0,380,15))
dev.off()
#-----------Zona 4----------------
jpeg('HZ4_M.jpg')
hist(Zona4$ml,main="Histograma magnitud sismos Zona SMG 4", 
xlab = "Magnitud (ml)",
ylab = "Frecuencia",
seq(2,4,0.25),
col="darkgreen")
dev.off()
#-----------------------------
jpeg('HZ4_P.jpg')
hist(Zona4$prof,main="Histograma profundidad sismos Zona SMG 4", 
xlab = "Profundidad (km)",
ylab = "Frecuencia",
col="gold",
seq(0,200, 25))
dev.off()
#--------------------------------
jpeg('HZ4_F.jpg')
hist(strtoi(Zona4$time),main="Histograma frecuencia sismos Zona SMG 4", 
xlab = "Día del año",
ylab = "Frecuencia",
col="blue",
seq(0,380,15))
dev.off()
#-----------Zona 5----------------
jpeg('HZ5_M.jpg')
hist(Zona5$ml,main="Histograma magnitud sismos Zona SMG 5", 
xlab = "Magnitud (ml)",
ylab = "Frecuencia",
seq(0,5,0.5),
col="darkgreen")
dev.off()
#-----------------------------
jpeg('HZ5_P.jpg')
hist(Zona5$prof,main="Histograma profundidad sismos Zona SMG 5", 
xlab = "Profundidad (km)",
ylab = "Frecuencia",
seq(0,250, 25),
col="gold")
dev.off()
#--------------------------------
jpeg('HZ5_F.jpg')
hist(strtoi(Zona5$time),main="Histograma frecuencia sismos Zona SMG 5", 
xlab = "Día del año",
ylab = "Frecuencia",
col="blue",
seq(0,380,15))
dev.off()
#-----------Zona 6----------------
jpeg('HZ6_M.jpg')
hist(Zona6$ml,main="Histograma magnitud sismos Zona SMG 6", 
xlab = "Magnitud (ml)",
ylab = "Frecuencia",
seq(1,5,0.5),
col="darkgreen")
dev.off()
#-----------------------------Algunos no superficiales
jpeg('HZ6_P.jpg')
hist(Zona6$prof,main="Histograma profundidad sismos Zona SMG 6", 
xlab = "Profunidad (km)",
ylab = "Frecuencia",
seq(0,250, 25),
col="gold")
dev.off()
#--------------------------------
jpeg('HZ6_F.jpg')
hist(strtoi(Zona6$time),main="Histograma frecuencia sismos Zona SMG 6", 
xlab = "Día del año",
ylab = "Frecuencia",
col="blue",
seq(0,380,15))
dev.off()
#-----------Zona 7----------------
jpeg('HZ7_M.jpg')
hist(Zona7$ml,main="Histograma magnitud sismos Zona SMG 7", 
xlab = "Magnitud (ml)",
ylab = "Frecuencia",
seq(2,5.5,0.5),
col="darkgreen")
dev.off()
#-----------------------------
jpeg('HZ7_P.jpg')
hist(Zona7$prof,main="Histograma profundidad sismos Zona SMG 7", 
xlab = "Profunidad (km)",
ylab = "Frecuencia",
seq(0,250, 25),
col="gold")
dev.off()
#--------------------------------
jpeg('HZ7_F.jpg')
hist(strtoi(Zona7$time),main="Histograma frecuencia sismos Zona SMG 7", 
xlab = "Día del año",
ylab = "Frecuencia",
col="blue",
seq(0,380,15))
dev.off()
#-----------Zona 8----------------
jpeg('HZ8_M.jpg')
hist(Zona8$ml,main="Histograma magnitud sismos Zona SMG 8", 
xlab = "Magnitud (ml)",
ylab = "Frecuencia",
seq(3,5,0.25),
col="darkgreen")
dev.off()
#-----------------------------
jpeg('HZ8_P.jpg')
hist(Zona8$prof,main="Histograma profundidad sismos Zona SMG 8", 
xlab = "Profundidad (km)",
ylab = "Frecuencia",
seq(0,60, 5),
col="gold")
dev.off()
#--------------------------------
jpeg('HZ8_F.jpg')
hist(strtoi(Zona8$time),main="Histograma frecuencia sismos Zona SMG 8", 
xlab = "Día del año",
ylab = "Frecuencia",
col="blue",
seq(0,380,15))
dev.off()


#Relacion profundidad-Magnitud
plot( (Zona3$prof), (Zona3$ml))
plot( (Zona7$prof), (Zona7$ml))

