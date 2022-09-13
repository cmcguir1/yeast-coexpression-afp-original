#Graphs histogram comparing the confidences of positive-positive gene pairs to positive negative gene pairs

comparePosNegPairs <- function(posFile,negFile) {
  posPairs <- read.csv(posFile)
  negPairs <- read.csv(negFile)
  
  lb <-rgb(107, 178, 255,maxColorValue=255,alpha=128)
  lg <-rgb(54, 173, 100,maxColorValue=255,alpha=128)
  p <- rgb(255, 110, 110,maxColorValue=255,alpha=128)
  
  legendlb <-rgb(107, 178, 255,maxColorValue=255,alpha=255)
  legendlg <- rgb(54, 173, 100,maxColorValue=255,alpha=255)
  legendp <- rgb(255, 110, 110,maxColorValue=255,alpha=255)
  
  numBreaks <- 24
  
  w <- 4
  
  adjust = 0.75
  posDen <- density(posPairs[,3],adjust=adjust)
  negDen <- density(negPairs[,3],adjust=adjust)
  
  
  plot(negDen,type="l",col=legendp,lwd=w,xlab="Confidence",ylab="Density",main="Pairs Confidence Distributions")
  lines(posDen,type="l",col=legendlg,lwd=w)
  polygon(negDen,col=p,border=legendp)
  polygon(posDen,col=lg,border=legendlg)
  
  legend("topright",c("Pos-Pos Pairs","Pos-Neg Pairs"),pch=15,col = c(legendlg,legendp),pt.cex = 2)
  
  
  
}


pos <- "C:\\Users\\colem\\SummerResearch2022\\Yeast Resources\\GraphResults\\Original_113x20x1\\Original_113x20x1_Pairs_PosPairs.csv"
neg <- "C:\\Users\\colem\\SummerResearch2022\\Yeast Resources\\GraphResults\\Original_113x20x1\\Original_113x20x1_Pairs_NegPairs.csv"
#pdf("PairsConfidenceDist.pdf",width=6,height=6)
comparePosNegPairs(posFile=pos,negFile=neg)
#dev.off()