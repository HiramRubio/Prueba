

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
datam <- data[ which (data$Zona!="NA"),]

var1 <- Zona0[Zona0$ml > 3.5,]		#Sismos con magnitud mayor a 3.5
var <- var1[var1$ml<5,]
hist(var$ml, main="Magnitud")
barplot(table(var$ml))
range(var$ml)				#Rango
breaks = seq(3.5,5.30,by=0.25)		#Breaks
ml.cut = cut(var$ml,breaks,right=FALSE)	#Aplicamos los quiebres a la data
ml.freq = table(ml.cut)				#Calculamos la frecuencia en cada uno
cbind(ml.freq)					#Lo mostramos en forma V
barplot(ml.freq)					#Gráfico de barras
h= hist(var$ml, main = "Magnitud", ylim=c(0,50), col="red", xlab="Magnitud, ml")
#Histograma y barra de tendencia
#lines(c(0,h$mids),c(0,h$counts), type = "b", pch = 20, col = "blue", lwd = 3)

#Grafico de prueba frecuencia acumulada
plot(c(0,h$mids), c(rev(cumsum(h$counts)),0), type = "b", col = "blue", pch = 20)

#Encontramos la frecuencia relativa
ml.relfreq = ml.freq / nrow(var) *100 
cbind(ml.freq, ml.relfreq) 

#La acumulamos
ml.cumfreq = cumsum(ml.relfreq)
ml.cumfreq

#Calculamos la frecuencia acumulada en orden inverso
cumfreq0 = rev(c(0, cumsum(ml.freq)))
cumfreq0

jpeg('LGR_NL.jpg')
plot(breaks, cumfreq0,            	# plot 
main="Frecuencia Acumulada",  	# título 
 xlab="Magnitud, ml",        		#etiqueta x
 ylab="Acumulado")   			# etiqueta y 
lines(breaks, cumfreq0)           	# unir los puntos 
dev.off()

#Mismo gráfico pero logaritmico
jpeg('LGR_L.jpg')
plot(breaks, log10(cumfreq0),            # plot 
main="Frecuencia Acumulada",  # título 
 xlab="Magnitud, ml",        #etiqueta x???axis 
 ylab="log(Acumulado)")   # etiqueta y???axis 
lines(breaks, log10(cumfreq0))           # unir los puntos 
dev.off()
n <- length(cumfreq0)-1

#Aproximación No Log 
jpeg('LGR_NLT.jpg')
reg = lm(cumfreq0[0:n] ~ breaks[0:n])
coefs = coefficients(reg)
eq = paste0("y = ", round(coefs[1],1), "*x ", round(coefs[2],1))
plot(breaks,cumfreq0, type = "b", col = "blue", pch = 20,main=eq)
abline(reg, col="red")
dev.off()

#Aproximación Log 
jpeg('LGR_LT.jpg')
reg = lm(log10(cumfreq0[0:n]) ~ breaks[0:n])
coefs = coefficients(reg)
eq = paste0("y = ", round(coefs[1],1), "*x ", round(coefs[2],1))
plot(breaks,log10(cumfreq0), type = "b", col = "blue", pch = 20,main=eq)
abline(reg, col="red")
dev.off()
