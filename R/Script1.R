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
hist(Zona0$ml,main="Histograma magnitud sismos Zona SMG 8", xlab = "ml" )
hist(Zona8$prof,main="Histograma profundidad sismos Zona SMG 8", xlab = "profunidad, km" )