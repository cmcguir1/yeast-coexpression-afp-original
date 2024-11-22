

plotAUCDists <- function(files,labels,graphName) {
  # Initializing Colors
  lightBlue <-rgb(107, 178, 255,maxColorValue=255,alpha=64)
  lightGreen <-rgb(54, 173, 100,maxColorValue=255,alpha=164)
  pink <- rgb(252, 3, 3,maxColorValue=255,alpha=64)
  purple <- rgb(120, 2, 171,maxColorValue=255,alpha=64)
  
  
  borderlb <-rgb(107, 178, 255,maxColorValue=255,alpha=255)
  borderlg <- rgb(54, 173, 100,maxColorValue=255,alpha=255)
  borderpk <- rgb(252, 3, 3,maxColorValue=255,alpha=255)
  borderpurp <- rgb(120, 2, 171,maxColorValue=255,alpha=255)
  
  colors <- c(lightGreen,pink,lightBlue,purple)
  borders <- c(borderlg,borderpk,borderlb,borderpurp)
  
  
  w <-5
  legendLabels <- c()
  
  for(i in 1:length(files)) {
    model <- read.csv(files[i])
    
    
    
    den <- density(model[,"AUC"])
    if(i == 1) plot(den,type="l",lwd=w,xlim=c(0.4,1),ylim=c(0,8),xlab="Area Under the Curve",ylab="Density",main=graphName)
    polygon(den,col=colors[i],border=borders[i],lwd=w)
    
    
    mean <- format(mean(model[,"AUC"]),digits=4)
    std <- format(sd(model[,"AUC"]),digits=4)
    #avgMean <- "Place Holder"
    #avgSd <- format(sd(avgDen),digits=3)
    #avgSd <- "Place Holder"
    legendLabels <- append(legendLabels,paste(labels[i]," Mean: ",mean,"; Std: ",std,sep=""))
  
  }
  
  legend("topleft",legendLabels,lty=1,lwd=4,seg.len = 4, col = borders)
  
  
}

dataFiles <- choose.files()
title <- "Net Hidden 80x80x80 Eval 2022 Onto"
labels <- c("Expr2007-Onto2007","Expr2007-Onto2022","Expr2022-Onto2007","Expr2022-Onto2022")
fileName <- "NetHidden_80x80x80_AllTerms.pdf"

pdf(fileName,width=10,height=6)
plotAUCDists(dataFiles,labels,graphName=title)
dev.off()



