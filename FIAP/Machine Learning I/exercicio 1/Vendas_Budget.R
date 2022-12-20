library(tidyverse)
library(readr)

url =  getURL("https://raw.githubusercontent.com/KValim/Projetcs/main/FIAP/Machine%20Learning%20I/exercicio%201/dataset/Vendas_2016a2018.csv")
df <- read_delim(url, delim = ";", escape_double = FALSE, trim_ws = TRUE)
df

str(df)

summary(df)


media_vendas = mean(df$Vendas)
media_vendas

dp_vendas = sd(df$Vendas)
dp_vendas


media_bud = mean(df$Budget_Advertising)
media_bud

dp_bud = sd(df$Budget_Advertising)
dp_bud


cv_vendas = dp_vendas/media_vendas
cv_vendas

cv_bud = dp_bud/media_bud
cv_bud




options (scipen = 999)
plot(df$Vendas ~ df$Budget_Advertising)
abline(modelo)

modelo = lm(df$Vendas ~ df$Budget_Advertising)
modelo


summary(modelo)


plot(df$Vendas ~ df$Budget_Advertising)
abline(modelo)


corr = cor.test(df$Vendas, df$Budget_Advertising)
corr


r2 = 0.8516129 * 0.8516129 
r2


df$vendas_estimada = 1060550.396 + 4.964 * df$Budget_Advertising
df


df$residuo = df$Vendas - df$vendas_estimada
df


summary(df$residuo)


media_residuo = mean(df$residuo)
media_residuo

dp_residuo = sd(df$residuo)
dp_residuo


df$residuo_padronizado = (df$residuo-media_residuo)/dp_residuo
df


hist(df$residuo)
hist(df$residuo_padronizado)


url2 =  getURL("https://raw.githubusercontent.com/KValim/Projetcs/main/FIAP/Machine%20Learning%20I/exercicio%201/dataset/Budget_2019.csv")
Budget_2019 <- read_delim(url2, delim = ";", escape_double = FALSE, trim_ws = TRUE)
Budget_2019



Budget_2019$vendas_estimadas = 1060550.396 + 4.964 * Budget_2019$Budget_Advertising
Budget_2019


sum(Budget_2019$vendas_estimadas)
