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
  model <- "MultiTerm_Modern_NetStruct_Labeled"
} else {
  terms <-read.csv("C:\\Users\\colem\\SummerResearch2022\\src\\PairwiseYeastNetwork\\SlimTerms_2007.csv")
  model <- "MultiTerm_NetStruct_PS_Labeled"
}







max_X <- 0
min_X <- 0
max_Y <- 0


green <-rgb(54, 173, 100,maxColorValue=255,alpha=64)
red <- rgb(255, 110, 110,maxColorValue=255,alpha=64)
purple <- rgb(120, 2, 171,maxColorValue=255,alpha=64)


b_green <- rgb(54, 173, 100,maxColorValue=255,alpha=255)
b_red <- rgb(255, 110, 110,maxColorValue=255,alpha=255)
b_purple <- rgb(120, 2, 171,maxColorValue=255,alpha=255)


pdf(paste(model,"_PairsDist_Labeled.pdf",sep=""),height=79*4,width=6)
par(mfrow=c(length(terms$GO.Term),1))
for(t in terms$GO.Term) {
  term <- str_replace(t,":","-")
  print(term)
  
  data <- read.csv(paste("C:\\Users\\colem\\SummerResearch2022\\Yeast Resources\\PairsSample\\",model,"\\",term,"_PairsSample_Labeled.csv",sep=""))
  posDen <- density(data[data$Label == '+',]$Scores)
  negDen <- density(data[data$Label == '-',]$Scores)
  agnDen <- density(data[data$Label == '0',]$Scores)
  
  max_y <- max(max(posDen$y),max(negDen$y),max(agnDen$y))
  plot(posDen,lwd=5,main=paste(term,nameMap[[term]],sep="\n"),xlab="Pairwise Confidence",ylim=c(0,max_y))
  
  polygon(posDen,col=green,border=b_green,lwd=5)
  polygon(negDen,col=red,border=b_red,lwd=5)
  polygon(agnDen,col=purple,border=b_purple,lwd=5)
  
  legend("topleft",legend=c("Pos Pairs","Neg Pairs","Agn Pairs"),fill=c(b_green,b_red,b_purple))
  
}
dev.off()
