plotAUCDist <- function(files,graphName) {
  fold1 <- read.csv(files[1])
  fold2 <- read.csv(files[2])
  fold3 <- read.csv(files[3])
  fold4 <- read.csv(files[4])
  
  lightBlue <-rgb(107, 178, 255,maxColorValue=255,alpha=64)
  lightGreen <-rgb(54, 173, 100,maxColorValue=255,alpha=164)
  pink <- rgb(255, 110, 110,maxColorValue=255,alpha=64)
  purple <- rgb(120, 2, 171,maxColorValue=255,alpha=64)
  white <- rgb(255, 255, 255,maxColorValue=255,alpha=64)
  
  
  borderlb <-rgb(107, 178, 255,maxColorValue=255,alpha=255)
  borderlg <- rgb(54, 173, 100,maxColorValue=255,alpha=255)
  borderpk <- rgb(255, 110, 110,maxColorValue=255,alpha=255)
  borderpurp <- rgb(120, 2, 171,maxColorValue=255,alpha=255)
  
  w <-5
  den1 <- density(fold1[,"AUC"])
  den2 <- density(fold2[,"AUC"])
  den3 <- density(fold3[,"AUC"])
  den4 <- density(fold4[,"AUC"])
  avgDen <- c(fold1[,"AUC"],fold2[,"AUC"],fold3[,"AUC"],fold4[,"AUC"])
  
  plot(den1,type="l",lwd=w,xlim=c(0,1),ylim=c(0,6),xlab="Area Under the Curve",ylab="Density",main=graphName)
  polygon(den1,col=lightBlue,border=borderlb,lwd=w)
  
  #plot(den2,type="l",lwd=w)
  polygon(den2,col=lightGreen,border=borderlg,lwd=w)
  
  #plot(den3,type="l",lwd=w)
  polygon(den3,col=pink,border=borderpk,lwd=w)
  
  #plot(den4,type="l",lwd=w)
  polygon(den4,col=purple,border=borderpurp,lwd=w)
  
  avgMean <- format(mean(avgDen),digits=4)
  #avgMean <- "Place Holder"
  avgSd <- format(sd(avgDen),digits=3)
  #avgSd <- "Place Holder"
  
  legend("topleft",c("Fold 1", "Fold 2","Fold 3","Fold 4", paste("Avg Mean: ",avgMean,sep=""),paste("Avg STD: ",avgSd,sep="")),lty=1,lwd=4,seg.len = 4, col = c(borderlb,borderlg,borderpk,borderpurp,white,white))
  
  
}
#Read in multiple files

files = choose.files(default=paste0(getwd(),"/*.*"))

currentWd = getwd()
setwd("C:/Users/colem/SummerResearch2022/Yeast Resources/Yeast Graphs")

name <- "Original"
struct <- "113x200x1"
type <- "Train"

graph <- paste(name,struct,type,sep=" ")
fileName <- paste(name,"_",struct,"_AUCDist_",type,".pdf",sep="")



#pdf(fileName,width=8,height=6)
plotAUCDist(files=files,graphName = graph)
#dev.off()
setwd(currentWd)
