
ensembleROC <- function(dataFile,labels,graphName) {
  getAUC <- function(data){
    
    decimalPlaces <- 3
    return(format(round(mean(data[,"Recall"]),decimalPlaces) , nsmall=decimalPlaces))
  }
  
  legendLabels <- c()
  w <- 4
  lt <- 1
  plot(c(0,1),c(0,1),lwd=w,col="#000000",main=graphName,type='l',xlab="False Positive Rate",ylab="Recall")
  
  for(i in 1:length(dataFiles)) {
  
    nn <- read.csv(dataFiles[i])
    nn <- nn[order(nn[,"Score"],decreasing = FALSE),]
    nn <- dplyr::filter(nn,Label!=0)
    
    
    
    colorsList <- c("#FC0303","#14A63B","#5D87F0","#7713BA","#FAEF16","#E09704")
    lines(nn[,"False.Positive.Rate"],nn[,"Recall"],lwd=w,col=colorsList[i],lty=lt)
    
    
    
    legendLabels <- append(legendLabels,paste(labels[i],"(AUC =",getAUC(nn),")"))
  }
  
  
  legend("bottomright",legendLabels,lwd=w,col=colorsList,seg.len = 4,lty=lt)
  
  
}

ensemblePR <- function(dataFile,labels,graphName) {
  getAveragePrecision <- function(precs){
    decimalPlaces <- 3
    return(format(round(mean(precs),decimalPlaces) , nsmall=decimalPlaces))
  }
  
  convexHull <- function(vec){
    for(i in length(vec):2) {
      if (vec[i] > vec[i-1]) {
        vec[i-1] <- vec[i]
      } 
    }
    return(vec)
  }
  
  legendLabels <- c()
  w <- 4
  lt <- 1
  
  for(i in 1:length(dataFiles)) {
    
    nn <- read.csv(dataFiles[i])
    nn <- nn[order(nn[,"Recall"],decreasing = FALSE),]
    nn <- dplyr::filter(nn,Label!=0)
    nn[,"Precision"] <- convexHull(nn[,"Precision"])
    
    
    
    colorsList <- c("#FC0303","#14A63B","#5D87F0","#7713BA","#FAEF16","#E09704")
    if (i == 1) plot(nn[,"Recall"],nn[,"Precision"],lwd=w,col=colorsList[i],lty=lt,main=graphName,type='l',xlab="Recall",ylab="Precision",log="x",ylim=c(0,1))
    else lines(nn[,"Recall"],nn[,"Precision"],lwd=w,col=colorsList[i],lty=lt)
    
    
    
    
    legendLabels <- append(legendLabels,paste(labels[i],"(Avg. Prec. =",getAveragePrecision(nn[,"Precision"]),")"))
  }
  
  
  legend("topright",legendLabels,lwd=w,col=colorsList,seg.len = 4,lty=lt)
  
  

  
  
  
  
  
}

createGraph <- function(dataFile,labels,graphName,fileName) {
  pdf(fileName,width=6,height=12)
  par(mfrow=c(2,1))
  ensembleROC(dataFile=dataFile,labels=labels,graphName=graphName)
  ensemblePR(dataFile=dataFile,labels=labels,graphName=graphName)
  dev.off()
}

displayGraph <- function(dataFile,labels,graphName,fileName) {
  
  
}

dataFiles <- choose.files()
labels <- c("Expr2007-Onto2007","Expr2007-Onto2022","Expr2022-Onto2007","Expr2022-Onto2022")

graphName <- "Net Hidden 80x80x80"
fileName <- "NetHidden_80x80x80.pdf"
createGraph(dataFiles,labels,graphName,fileName)

displayGraph(dataFiles,labels,graphName,fileName)








