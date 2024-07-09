source("C:/Users/colem/SummerResearch2022/R Scripts/StringFunctions.R")
library(stringr)
library(hash)

names <- read.csv("C:\\Users\\colem\\SummerResearch2022\\src\\PairwiseYeastNetwork\\TermNameDict.csv")
nameMap <- hash()

for(i in 1:nrow(names)){
  nameMap[[names[i,1]]] <- names[i,2]
}

terms <-read.csv("C:\\Users\\colem\\SummerResearch2022\\src\\PairwiseYeastNetwork\\SlimTerms_2007.csv")

model <- "MultiTerm_Modern_NetStruct"

max_X <- 0
min_X <- 0
max_Y <- 0
for(t in terms$GO.Term) {
  term <- str_replace(t,":","-")
  print(term)
  
  data <- read.csv(paste("C:\\Users\\colem\\SummerResearch2022\\Yeast Resources\\PairsSample\\",model,"\\",term,"_PairsSample.csv",sep=""))
  den <- density(data$Scores)
  plot(den,lwd=5,main=paste(term,nameMap[[term]],sep="\n"))
  
}
