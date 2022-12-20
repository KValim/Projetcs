# regressão logistica

# libs
library(tidyverse)
library(summarytools)
library(gmodels)
library(fastDummies)

library(readr)
df = read_delim("C:/Users/KAIQUEHENRIQUEVALIM/Desktop/arq_inadimplencia.csv", 
                 delim = ";", 
                escape_double = FALSE, 
                trim_ws = TRUE)

df

# estrutura da base
str(df)


# mudar o formato das variaveis quantitativas para qualitativas
df$cliente  = factor (df$cliente )
df$Resposta = factor (df$Resposta)
df$atrasos = factor (df$atrasos, ordered=TRUE)
df$temporel = factor (df$temporel, ordered=TRUE)
df$valorfatura = factor (df$valorfatura, ordered=TRUE)
df$p_gastoalim = factor (df$p_gastoalim, ordered=TRUE) 
df$regiaorisco = factor (df$regiaorisco)
df$rendamensal = factor (df$rendamensal, ordered=TRUE)

df

# nao mostrar os resultados na notacao cientifica
options(scipen = 999)

# tabela de contigencia
CrossTable(df$Resposta, df$atrasos, chisq=TRUE)
# a base é dividade entre adimplentes e inadimplentes
# 22% do atraso tipo 1, 29% do  2, 25% do 3 e 23% do 4

CrossTable(df$Resposta, df$temporel, chisq=TRUE)
CrossTable(df$Resposta, df$valorfatura, chisq=TRUE)
CrossTable(df$Resposta, df$p_gastoalim, chisq=TRUE)
CrossTable(df$Resposta, df$regiaorisco, chisq=TRUE)
CrossTable(df$Resposta, df$rendamensal, chisq=TRUE)

# a inadimplencia tem relação com todas as variaveis, portanto nenhuma será removida.
# o próximo passo é a criação das variaveis dummies. fastndummies



# variaveis preditoras
var_preditoras <- df %>%
  select(atrasos,temporel,valorfatura,p_gastoalim,regiaorisco,rendamensal)

# criar variaveis dummies
library(fastDummies)
# criar variaveis dummies usando fastdummies
# o fastdummies só funciona  graças ao passo no inicio de transformar as variaveis para factor
var_dummies <- dummy_cols(var_preditoras, remove_first_dummy = TRUE,
                          select_columns = c('atrasos','temporel','valorfatura','p_gastoalim',
                                             'regiaorisco','rendamensal'))

#View(var_dummies)
# apagar as variaveis originais
var_dummies$atrasos = NULL
var_dummies$temporel = NULL
var_dummies$valorfatura = NULL
var_dummies$p_gastoalim = NULL
var_dummies$regiaorisco = NULL
var_dummies$rendamensal = NULL

# merge da var Resposta com os dummies
# criar a base de dados para o modelo
df <- df %>%
  select(Resposta) %>%
  cbind(var_dummies)

#View(df)

# dividir a amostra em treino e validacao
set.seed(2019)
train <- sample(nrow(df), 0.7*nrow(df), replace = FALSE)
TrainSet <- df[train,]
ValidSet <- df[-train,]


# é importante verificar se a proporção da variavel resposta está bem distribuida entre treino e teste
# tabela de frequencia da amostra treino e validacao
# verificar se a distribuicao da variavel resposta é igual nas duas amostras
freq(TrainSet$Resposta)
freq(ValidSet$Resposta)

#GLM Modelos lineares Generalizados (General Linear Models)
# Regressao Logistica
Mod_Log<- glm(Resposta ~ .,
              TrainSet, family=binomial(link=logit))
summary(Mod_Log)
# distribuição do residuo = erro do modelo
# a única variavel que não é significativa é a valorfatura_2 com p_valor > 0.05
# o idela é retirar essa var com stepwise ou na mão, mas a professora está com preguiça

# aplicando na base de treino
# estimar a probabilidade do cliente torna-se inadimplente
TrainSet$probabilidade = fitted(Mod_Log)

# como o modelo chegou na probabilidade?
# para calcular a prob,. você tem que somar e multiplicar as  e depois jogar na formula de exp


# Curva ROC
library(ROCit)

## rocit object
# tres metodos
rocit_emp <- rocit(score = TrainSet$probabilidade,
                   class = TrainSet$Resposta,
                   method = "emp")
rocit_bin <- rocit(score = TrainSet$probabilidade,
                   class = TrainSet$Resposta,
                   method = "bin")
rocit_non <- rocit(score = TrainSet$probabilidade,
                   class = TrainSet$Resposta,
                   method = "non")



summary(rocit_emp)
summary(rocit_bin) #maior AUC
summary(rocit_non)

## Plot ROC curve
plot(rocit_emp, col = c(1,"gray50"),
     legend = FALSE, YIndex = FALSE)
lines(rocit_bin$TPR~rocit_bin$FPR,
      col = 2, lwd = 2)
lines(rocit_non$TPR~rocit_non$FPR,
      col = 4, lwd = 2)
legend("bottomright", col = c(1,2,4),
       c("Empirical ROC", "Binormal ROC",
         "Non-parametric ROC"), lwd = 2)

# a linha tracejada representa um modelo de 50% de chance de acerto, toss coin
# o binomial foi o melhor modelo com a maior AUC, de 87.83%

#AUC (Area Under the Curve) da curva ROC
ciAUC(rocit_emp)


# regra do ponto de corte
# a definição do parametro varia, mas basicamente acompanha a proporção da variavel resposta.
# como a base se divide em 50% inadimp e 50% adimp, o ponto de corte é igual 0,5

# o teste de KS é um método estatistico para definir o melhor ponto de corte
# o ponto  de corte do teste é aonde a existe a maior distancia entre as duas curvas

# Teste Kolmogorov-Smirnov (KS)
#A estatistica de Kolmogorov-Smirnov quantifica a distancia entre a funcao distribuicao
#empirica da amostra e a funcao distribuicao acumulada da distribuicao de referencia ou
#entre as funcoes distribuicao empirica de duas amostras.

rocit = rocit(score=TrainSet$probabilidade, TrainSet$Resposta)
ksplot = ksplot(rocit)
corte = ksplot$`KS Cutoff`
corte


# ponto de corte eh 0.50.Se a predito (probabilidade) >= 0.50 entao a previsao eh 1 e 0 caso contrario
#TrainSet$fx_predito <- cut(TrainSet$probabilidade, breaks=c(0,corte,1), right=F)
TrainSet$fx_predito <- cut(TrainSet$probabilidade, breaks=c(0,0.50,1), right=F)

# matriz de confusao ou classficacao
MC_log_treino <- table(TrainSet$Resposta, TrainSet$fx_predito , deparse.level = 2) # montar a matriz de confusao  
show(MC_log_treino) # mostra os resultados  
ACC_log = sum(diag(MC_log_treino))/sum(MC_log_treino)*100 # calcula a acuracia  
show(ACC_log) # mostra a acuracia  
print(prop.table(table(TrainSet$Resposta,TrainSet$fx_predito),1),digits=2)




# Amostra de validacao
ValidSet$probabilidade <- predict(Mod_Log,ValidSet,type = "response")
summary(ValidSet$probabilidade)   

# utilize o mesmo ponte de corte utilizado na amostra treino
ValidSet$fx_predito <- cut(ValidSet$probabilidade, breaks=c(0, 0.50, 1), right=F)


# matriz de confusao ou classficacao
MC_test_log <- table(ValidSet$Resposta, ValidSet$fx_predito , deparse.level = 2) # montar a matriz de confusao  
show(MC_test_log) # mostra os resultados  
ACC_log = sum(diag(MC_test_log))/sum(MC_test_log)*100 # calcula a acuracia  
show(ACC_log) # mostra a acuracia  
print(prop.table(table(ValidSet$Resposta,ValidSet$fx_predito),1),digits=2)