library(tidyverse)
library(readxl)
library(ggplot2)
library(readr)
library(summarytools)
library(gmodels)
library(corrplot)
library(fastDummies)

df = read_delim("C:\\Users\\KAIQUEHENRIQUEVALIM\\Documents\\FIAP\\Machine Learning I\\Bike_Sharing.csv",
                         delim = ",",
                         escape_double = FALSE,
                         trim_ws = TRUE)
View(df)

str(df)
summary(df)
# tomar cuidado com medidas que não são númericas, mas foram convertidas em números para inserção no modelo.
# por exemplo, não faz sentido a calcular a média da season, não existe temporada 2.497

df$season = as.factor(df$season) # muda var de quantitativa para qualitativa
summary(df)
