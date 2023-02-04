library(tidyverse)
library(readxl)
library(ggplot2)
library(readr)
library(summarytools)
library(gmodels)
library(corrplot)
library(fastDummies)
library(PerformanceAnalytics)
library(RCurl)

url =  getURL("https://raw.githubusercontent.com/KValim/Projetcs/main/FIAP/Machine%20Learning%20I/lista%201/dataset/Bike_Sharing.csv")
df = read.csv(text = url)

str(df)
summary(df)
# tomar cuidado com medidas que não são númericas, mas foram convertidas em números para inserção no modelo.
# por exemplo, não faz sentido a calcular a média da season, não existe temporada 2.497

df$season = factor(df$season, order = TRUE) # muda var de quantitativa para qualitativa
df$yr = factor(df$yr)
df$mnth = factor(df$mnth, order = TRUE)
df$holiday = factor(df$holiday)
df$weekday = factor(df$weekday, order = TRUE)
df$workingday = factor(df$workingday)
df$weathersit = factor(df$weathersit)
summary(df)

str(df)



# seleção das vars. quanti
var_num = df %>%
  select(temp, atemp, hum, windspeed, cnt)


# seleção das vars. dummie
var_dummy = df %>%
  select(yr, holiday, workingday)


# seleção das vars. quali
var_qualo = df %>%
  select(season, mnth, weekday, weathersit)



# analise exploratória quantitativos
# histograma cnt
hist(df$cnt)

# no histograma não da é possível detectar outliers
# para isso é utilizado o boxplot
# em todas as vars quantitativas
boxplot(df$temp)
boxplot(df$atemp)
boxplot(df$hum) # tem outlier.. humidade muito baixa; sensação de deserto, deve alugar menos
boxplot(df$windspeed) # tem outlier.. ventos fotes; difícil pedalar, deve alugar menos
boxplot(df$cnt)
boxplot(df$temp)


# gráfico de dispersão
plot(df$cnt ~ df$temp)
plot(df$cnt ~ df$atemp)
plot(df$cnt ~ df$hum)
plot(df$cnt ~ df$windspeed)     


# correlação de pearson
corr_temp = cor.test(df$cnt, df$temp); corr_temp
corr_atemp = cor.test(df$cnt, df$atemp); corr_atemp
corr_hum = cor.test(df$cnt, df$hum); corr_hum
corr_windspeed = cor.test(df$cnt, df$windspeed); corr_windspeed


# matriz de correlação
mc = cor(var_num); mc


# gráfico de correlação
corrplot(mc, type = 'upper', method = 'number')


# figura do PerformAnalytics
chart.Correlation(var_num, histogram = TRUE)



# analise exploratório dos dados qualitativos
freq(df$season)
freq(df$yr)
freq(df$mnth)
freq(df$weekday)
freq(df$weathersit)


# gráfico de uma var. quantitativa e qualitativa
boxplot(df$cnt ~ df$season)
boxplot(df$cnt ~ df$weekday)
boxplot(df$cnt ~ df$mnth)
boxplot(df$cnt ~ df$weathersit)


# teste qui-quadrado para identificar associação

# tranformar cnt em var qualitativa
summary(df$cnt)
df$fx_cnt = cut(df$cnt, breaks = c(22, 3152, 4548, 5956, Inf), right = TRUE, include.lowest = TRUE, dig.tab = 10)
freq(df$fx_cnt)


# calçcular o teste qui-quadrado
CrossTable(df$fx_cnt, df$season, chist = TRUE)
CrossTable(df$fx_cnt, df$weekday, chist = TRUE)


# criar as vars dummie
var_quali_dummies = dummy_cols(var_qualo, remove_first_dummy = TRUE, select_columns = c('season', 'mnth', 'weekday', 'weathersit'))


var_quali_dummies$season = NULL
var_quali_dummies$mnth = NULL
var_quali_dummies$weekday = NULL
var_quali_dummies$weathersit = NULL

var_quali_dummies


# merge bases

df1 = cbind(var_num, var_dummy, var_quali_dummies)
df1


# modelo de regressao linear multipla
modelo1 = lm(df1$cnt ~ df1$temp)
summary(modelo1)

# exemplo de colinearidade
modelo2 = lm(df1$cnt ~ df1$temp + df$atemp)
summary(modelo2)

# exemplo de uso da variavel independente qualitativa
modelo3 = lm(df1$cnt ~ df1$season_2 + df1$season_3 + df1$season_4)
summary(modelo3)


modelo4 = lm(cnt ~ ., data = df1)
summary(modelo4)


modelo4_stepwise = step(modelo4, direction = 'both')
summary(modelo4_stepwise)




# dividir o modelo em duas amostras
set.seed(2021)
train = sample(nrow(df1), 0.7*nrow(df1), replace = FALSE)
TrainSet = df1[train,]
ValidSet = df1[-train,]

# medidas resumop da variavel resposta na amostra treino
summary(TrainSet$cnt)
# medidas resumop da variavel resposta na amostra validação
summary(ValidSet$cnt)

# importante checar se a médias nas nos dois dfs são semelhantes



# regressão linear multiplca
modelo5 =  lm(cnt ~ ., data = TrainSet)
summary(modelo5)

modelo5_stepwise = step(modelo5, direction = 'both')
summary(modelo5_stepwise)



# calcular a raiz do erro quadratico medio
# valor estimado pelo modelo
TrainSet$Val_pred = predict(modelo5_stepwise,interval = "prediction",
                             level = 0.95,data=TrainSet) 

# resdiduo do modelo
TrainSet$residuo = resid(modelo5_stepwise)
# residuo padronizado do modelo
TrainSet$rp = rstandard(modelo5_stepwise)

# histograma dos residuos
hist(TrainSet$rp)

# raiz do Erro quadratico medio na amostra de treino
mse = mean((TrainSet$cnt - TrainSet$Val_pred)^2)
sqrt(mse)

# calcular a previsao da cnt na base de validacao
# valor estimado pelo modelo


ValidSet$Val_pred = predict(modelo5_stepwise,interval = "prediction",
                             level = 0.95, newdata=ValidSet) 


# raiz do Erro quadratico medio na amostra de treino
mse = mean((ValidSet$cnt - ValidSet$Val_pred)^2)
sqrt(mse)



plot(ValidSet$cnt ~ ValidSet$Val_pred[,'fit'])


#library
library(latticeExtra)

x <- 1:length(ValidSet$cnt)
var1 <- ValidSet$cnt
var2 <- ValidSet$Val_pred[,'fit']
data <- data.frame(x,var1,var2)



plot(x, var1, type="l",  col="red", xlab="", ylab="bikes")
# Add a line
lines(x, var2,  col="blue", type="l")
# Add a legend

legend("topleft", legend=c("cnt", "prediction"),
       col=c("red", "blue"), lty=1:1, cex=0.8)
