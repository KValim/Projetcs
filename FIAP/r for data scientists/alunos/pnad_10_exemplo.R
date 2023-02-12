
##############################  1 Entrega ###########################

library(readxl)
pnad_10 <- read_excel("D:/FIAP/Data Science/R for data science/pnad_10.xlsx")
View(pnad_10)

names(pnad_10)
dim(pnad_10)


pnad_10$Rendim.efetivoqqtrabalho <- round(as.integer(pnad_10$Rendim.efetivoqqtrabalho,digits=3))
pnad_10$Rendim.efetivotrab.princ <- as.numeric(pnad_10$Rendim.efetivotrab.princ)
pnad_10$Rendim.habitualqqtrabalho <- as.numeric(pnad_10$Rendim.habitualqqtrabalho)# convertendo para numerica

library(dplyr)
table(pnad_10$UF)

df <-pnad_10[,c('Rendim.habitualqqtrabalho','Rendim.efetivotrab.princ','Rendim.efetivoqqtrabalho','UF','Sexo')]
df

dim(df)

# na.omit excluir todas as linhas que possui NA - cuidado.
df1 <- na.omit(df)
dim(df1)


str(df1)

grupo1 <-summarise(group_by(df1,UF,Sexo),
           renda = mean(Rendim.habitualqqtrabalho),
           Frequencia = n())

grupo1


library(plotly)
library(ggplot)

dispersao_renda <- ggplot(grupo1,aes(x=renda, y=UF, color=Sexo))+
  geom_point()

dispersao_renda



