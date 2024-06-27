plotAUCDist_Single <- function(file,graphName) {
  fold1 <- read.csv(file)
  
  lightBlue <-rgb(107, 178, 255,maxColorValue=255,alpha=64)
  
  
  
  borderlb <-rgb(107, 178, 255,maxColorValue=255,alpha=255)
  white <- rgb(255, 255, 255,maxColorValue=255,alpha=64)
  
  w <-5
  den1 <- density(fold1[,"AUC"])
  
  plot(den1,type="l",lwd=w,xlim=c(0,1),ylim=c(0,8),xlab="Area Under the Curve",ylab="Density",main=graphName)
  polygon(den1,col=lightBlue,border=borderlb,lwd=w)
  
  #plot(den2,type="l",lwd=w)
  #polygon(den2,col=lightGreen,border=borderlg,lwd=w)
  
  #plot(den3,type="l",lwd=w)
  #polygon(den3,col=pink,border=borderpk,lwd=w)
  
  #plot(den4,type="l",lwd=w)
  #polygon(den4,col=purple,border=borderpurp,lwd=w)
  
  avgMean <- format(mean(fold1[,"AUC"]),digits=4)
  std <- format(sd(fold1[,"AUC"]),digits=4)
  #avgMean <- "Place Holder"
  #avgSd <- format(sd(avgDen),digits=3)
  #avgSd <- "Place Holder"
  
  legend("topleft",c(paste("Mean AUC:",avgMean),paste("AUC STD:",std)),lty=1,lwd=4,seg.len = 4, col = c(borderlb,white))
  
  
}

dataFile <- file.choose()

graphName <- "Net 500x200x100 Rep 0"
pdf("MultiTerm_Net_500x200x100_Rep_0_AUC_Dist.pdf",width=10,height=6)
plotAUCDist_Single(file=dataFile,graphName=graphName)
dev.off()
