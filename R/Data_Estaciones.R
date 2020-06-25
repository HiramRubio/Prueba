
data <- read.csv("C:/Users/HRV/Desktop/Post-U/Trabajo/Prueba/Data/Mex_Sup_estaciones.csv")

#Observacion de las estaciones que más registran sismos en la zona
categories0 <- sort(table(data$Est), decreasing = TRUE)
categories1 <- length(table(data$Est))
categories2 <- unique(data$Est) 

#Valiamos las 5 estaciones mas utilizadas
cnt = 0
for(i in names(categories0)){
	if(cnt>=5) break
	else {
		#Seleccion de una estacion en particular y distancia
		Est_0 <- data[ which (data$Est== i ),]
		Est_D <- unique(Est_0$Dist..km.)
		print(i) 
		print(range(Est_D))
		
		#Hisograma para verificar
		if(cnt==4){
		hist(Est_D,main="Rango Sensibilidad (Est: xxx)", 
		xlab = "Distancia (km)",
		ylab = "Frecuencia",
		col="darkgreen")
		}
		cnt = cnt +1
		}
	}



