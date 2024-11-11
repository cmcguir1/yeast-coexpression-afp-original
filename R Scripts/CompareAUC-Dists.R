lightBlue <-rgb(107, 178, 255,maxColorValue=255,alpha=64)
lightGreen <-rgb(54, 173, 100,maxColorValue=255,alpha=164)
pink <- rgb(255, 110, 110,maxColorValue=255,alpha=64)
purple <- rgb(120, 2, 171,maxColorValue=255,alpha=64)
white <- rgb(255, 255, 255,maxColorValue=255,alpha=64)


borderlb <-rgb(107, 178, 255,maxColorValue=255,alpha=255)
borderlg <- rgb(54, 173, 100,maxColorValue=255,alpha=255)
borderpk <- rgb(255, 110, 110,maxColorValue=255,alpha=255)
borderpurp <- rgb(120, 2, 171,maxColorValue=255,alpha=255)

colors <- c(lightBlue,lightGreen,pink,purple)
borders <- c(borderlb,borderlg,border,pink,borderpurp)

plotAUCDists <- function(files,graphName) {
  
  w <-5
  legendLabels <- c()
  
  for(i in 1:length(files)) {
    model <- read.csv(files[i])
    
    
    
    den <- density(model[,"AUC"])
    if(i == 1) plot(den,type="l",lwd=w,xlim=c(0,1),ylim=c(0,8),xlab="Area Under the Curve",ylab="Density",main=graphName)
    polygon(den,col=colors[i],border=borders[i],lwd=w)
    
    
    mean <- format(mean(fold1[,"AUC"]),digits=4)
    std <- format(sd(fold1[,"AUC"]),digits=4)
    #avgMean <- "Place Holder"
    #avgSd <- format(sd(avgDen),digits=3)
    #avgSd <- "Place Holder"
    legendLabels <- append(legendLabels,paste("Mean: ",mean,"; Std: ",std,sep=""))
  
  }
  
  legend("topleft",legendLabels,lty=1,lwd=4,seg.len = 4, col = borders)
  
  
}


