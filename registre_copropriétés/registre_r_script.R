
# chargement de la library tidyverse nécessaire pour la plupart des opérations
library(tidyverse)

setwd(dirname(rstudioapi::getActiveDocumentContext()$path))

#Chargement du dataset correspondant à Lyon :
data <- read_csv("registre_lyon.csv")

#Creation de la liste des arrondissements de lyon
list_lyon <- list("LYON 1ER", "LYON 2EME", "LYON 3EME", "LYON 4EME", "LYON 5EME", "LYON 6EME", "LYON 7EME", "LYON 8EME", "LYON 9EME")

#Tracé des histogrammes avec une autre méthode de sélection des lignes au sein d'une colonnne'
par(mfrow=c(3,3))
for (i in 1: 9) {
  lyon_tmp <- data[data$'Commune du représentant légal' == list_lyon[[i]],]
  hist(lyon_tmp$"Nombre total de lots", xlab="Nombre de lots", main=paste("Arrondissement ",as.character(i)),breaks=c(0,11,31,51,101,200,max(lyon_tmp$"Nombre total de lots")))
}



