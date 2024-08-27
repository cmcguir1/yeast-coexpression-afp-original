source("C:/Users/colem/SummerResearch2022/R Scripts/StringFunctions.R")
library(stringr)
library(hash)

names <- read.csv("C:\\Users\\colem\\SummerResearch2022\\src\\PairwiseYeastNetwork\\TermNameDict.csv")
nameMap <- hash()

for(i in 1:nrow(names)){
  nameMap[[str_replace(names[i,1],":","-")]] <- names[i,2]
}

modern <- T
if (modern) {
  terms <-read.csv("C:\\Users\\colem\\SummerResearch2022\\src\\PairwiseYeastNetwork\\SlimTerms_2023.csv")
  model <- "MultiTerm_Modern_NetStruct"
  
} else {
  terms <-read.csv("C:\\Users\\colem\\SummerResearch2022\\src\\PairwiseYeastNetwork\\SlimTerms_2007.csv")
  model <- "MultiTerm_NetStruct_PS"
}

max_X <- 0
min_X <- 0
max_Y <- 0

blue <-rgb(50, 80, 255,maxColorValue=255,alpha=64)
b_blue <-rgb(50, 80, 255,maxColorValue=255,alpha=255)

pdf(paste(model,"_PairsDist.pdf",sep=""),height=79*4,width=6)
par(mfrow=c(length(terms$GO.Term),1))
for(t in terms$GO.Term) {
  term <- str_replace(t,":","-")
  print(term)
  
  data <- read.csv(paste("C:\\Users\\colem\\SummerResearch2022\\Yeast Resources\\PairsSample\\",model,"\\",term,"_PairsSample.csv",sep=""))
  den <- density(data$Scores)
  plot(den,lwd=5,main=paste(term,nameMap[[term]],sep="\n"),xlab="Pairwise Confidence")
  polygon(den,col=blue,border=b_blue,lwd=5)
  
}
dev.off()
