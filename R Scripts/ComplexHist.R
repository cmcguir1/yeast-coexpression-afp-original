plotAUCDist <- function(files,graphName) {
  fold1 <- read.csv(files[1])
  fold2 <- read.csv(files[2])
  fold3 <- read.csv(files[3])
  fold4 <- read.csv(files[4])
  
  lightBlue <-rgb(107, 178, 255,maxColorValue=255,alpha=64)
  lightGreen <-rgb(54, 173, 100,maxColorValue=255,alpha=164)
  pink <- rgb(255, 110, 110,maxColorValue=255,alpha=64)
  purple <- rgb(120, 2, 171,maxColorValue=255,alpha=64)
  
  
  borderlb <-rgb(107, 178, 255,maxColorValue=255,alpha=255)
  borderlg <- rgb(54, 173, 100,maxColorValue=255,alpha=255)
  borderpk <- rgb(255, 110, 110,maxColorValue=255,alpha=255)
  borderpurp <- rgb(120, 2, 171,maxColorValue=255,alpha=255)
  
  w <-5
  den1 <- density(fold1[,"AUC"])
  den2 <- density(fold2[,"AUC"])
  den3 <- density(fold3[,"AUC"])
  den4 <- density(fold4[,"AUC"])
  
  plot(den1,type="l",lwd=w,xlim=c(0,1),ylim=c(0,5),xlab="Area Under the Curve",ylab="Density",main=graphName)
  polygon(den1,col=lightBlue,border=borderlb,lwd=w)
  
  #plot(den2,type="l",lwd=w)
  polygon(den2,col=lightGreen,border=borderlg,lwd=w)
  
  #plot(den3,type="l",lwd=w)
  polygon(den3,col=pink,border=borderpk,lwd=w)
  
  #plot(den4,type="l",lwd=w)
  polygon(den4,col=purple,border=borderpurp,lwd=w)
  
  legend("topright",c("Fold 1", "Fold 2","Fold 3","Fold 4"),lty=1,lwd=4,seg.len = 4, col = c(borderlb,borderlg,borderpk,borderpurp))
  
  
}
#Read in multiple files

files = choose.files(default=paste0(getwd(),"/*.*"))

currentWd = getwd()
setwd("C:/Users/colem/SummerResearch2022/Yeast Resources/Yeast Graphs")

graph <- "Original 113x200x100x50x92"
fileName <- "Original_113x200x100x50x92_AUCDist_Train.pdf"



pdf(fileName,width=8,height=6)
plotAUCDist(files=files,graphName = graph)
dev.off()
setwd(currentWd)
