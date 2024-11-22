
termData <- read.csv(file.choose())

g <-rgb(54, 173, 100,maxColorValue=255,alpha=164)
r <- rgb(252, 3, 3,maxColorValue=255,alpha=64)
gb <- rgb(54, 173, 100,maxColorValue=255,alpha=255)
rb <- rgb(252, 3, 3,maxColorValue=255,alpha=255)

w <- 3
a <- 1

pdf("2007vs2022_PairCorrelationDistributrion.pdf",width=8,height=6*nrow(termData))
par(mfrow=c(nrow(termData),1))
for(i in 1:nrow(termData)) {
  term <- termData$Go.Term[i]
  file <- paste("C:\\Users\\colem\\SummerResearch2022\\Yeast Resources\\CorrelationData\\GO",substring(term,4,11),"_Pairs.csv",sep="")
  data <- read.csv(file)
  print(term)
  ogDen <- density(data$X2007,adjust=a)
  modDen <- density(data$X2022,adjust=a)
  xMin <- min(min(ogDen$x),min(modDen$x))
  xMax <- max(max(ogDen$x),max(modDen$x))
  yMax <- max(max(ogDen$y),max(modDen$y))
  
  plot(ogDen,ylim=c(0,yMax),xlim=c(xMin,xMax),main=paste(term,termData$Name[i],sep="\n"),ylab="Density",xlab="Pair Z-score")
  polygon(ogDen,col=g,border=gb,lwd=w)
  polygon(modDen,col=r,border=rb,lwd=w)
  legend("topright",legend=c(
    paste("KS Statistic:",termData$KS.Statistic[i]),
    paste("KS p-value:",termData$KS.P.Value[i]),
    paste("2007 Annotations:",termData$X2007.Genes[i]),
    paste("2022 Annotations:",termData$X2022.Genes[i]))
  )
  
  
}
dev.off()
