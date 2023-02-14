
plotROC <- function(files,graphName) {
  width = 4
  decimalPlaces = 3
  colorsList <- c("#FC0303","#14A63B","#5D87F0","#7713BA","#FAEF16","#E09704")
  
  #Initialize lists that will store information for the legend
  legendLabels <- c()
  legendAUC <- c()
  
  #Reads in the first element of the files collection
  data <- read.csv(files[1])
  #Sorts data table by the Score column in ascending order
  data <- data[order(data[,"Score"],decreasing = FALSE),]
  #Creates a plot of the first data series
  plot(data[,"False.Positive.Rate"], data[,"Recall"], ylim= c(0,1), type="l", col=colorsList[1],
       lwd=width, main=graphName, xlab="False Positive Rate", ylab = "Recall")
  
  #Calculates AUC for first curve, the format function rounds the AUC off at decimal Places
  legendAUC <- append(legendAUC,format(round(mean(data[,"Recall"]),decimalPlaces) , nsmall=decimalPlaces))
  legendLabels <- append(legendLabels,paste("Fold 1 (AUC =",legendAUC[1],")"))
  
  #Draws black linear line to represent the control
  lines(c(0,1),c(0,1),lwd=width)
  
  #Loops over rest of data files
  for (i in 2:length(files)) {
    #Read in data file, then sort table by score
    data <- read.csv(files[i])
    data <- data[order(data[,"Score"],decreasing = FALSE),]
    
    #Plot data from table
    lines(data[,"False.Positive.Rate"],data[,"Recall"],lwd=width,col=colorsList[i])
    
    #Calculate AUC, then add to legends collections
    legendAUC <- append(legendAUC,format(round(mean(data[,"Recall"]),decimalPlaces) , nsmall=decimalPlaces))
    legendLabels <- append(legendLabels,paste("Fold",i,"(AUC =",legendAUC[i],")"))
  }
  
  #Adds legend
  legend("bottomright",legendLabels,lty=1,lwd=width, seg.len = 4,col = colorsList)
  
  
}


plotPrecRecall <- function(files,graphName) {
  width = 4
  decimalPlaces = 3
  colorsList <- c("#FC0303","#14A63B","#5D87F0","#7713BA","#FAEF16","#E09704")
  
  #Initialize lists that will store information for the legend
  legendLabels <- c()
  legendAUC <- c()
  
  #Reads in the first element of the files collection
  data <- read.csv(files[1])
  #Sorts data table by the Score column in ascending order
  data <- data[order(data[,"Score"],decreasing = FALSE),]
  
  #These two for loops stair step the data
  for(i in length(data[,"Recall"]):2) {
    if(data[i,"Precision"] < data[i-1,"Precision"]) data[i,"Precision"] <- data[i-1,"Precision"]
  }
  
  for(i in 1:(length(data[,"Recall"])-1)) {
    if(data[i,"Precision"] > data[i+1,"Precision"]) data[i+1,"Precision"] <- data[i,"Precision"]
  }
  
  #Creates a plot of the first data series
  plot(data[,"Recall"], data[,"Precision"], ylim= c(0,1), type="l", col=colorsList[1],
       lwd=width, main=graphName, xlab="Recall", ylab = "Precision",log='x')
  
  #splice <- data[,7:8]
  #splice <- data[,"Precision":"Recall"]
  splice <- data[,which(colnames(data)=="Precision"):which(colnames(data)=="Recall")]
  uSplice <- unique(splice)
  
  
  
  
  #Calculates AUC for first curve, the format function rounds the AUC off at decimal Places
  legendAUC <- append(legendAUC,format(round(mean(uSplice[,1]),decimalPlaces) , nsmall=decimalPlaces))
  legendLabels <- append(legendLabels,paste("Fold 1 (AUC =",legendAUC[1],")"))
  
  #Draws black linear line to represent the control
  #control <- sum(as.numeric(data[,3]))/length(data[,3])
  #lines(c(0,1),c(control,control),lwd=width)
  
  #Loops over rest of data files
  for (i in 2:length(files)) {
    #Read in data file, then sort table by score
    data <- read.csv(files[i])
    data <- data[order(data[,"Score"],decreasing = FALSE),]
    
    #These two for loops stair step the data
    for(j in length(data[,"Recall"]):2) {
      if(data[j,"Precision"] < data[j-1,"Precision"]) data[j,"Precision"] <- data[j-1,"Precision"]
    }
    
    for(j in 1:(length(data[,"Recall"])-1)) {
      if(data[j,"Precision"] > data[j+1,"Precision"]) data[j+1,"Precision"] <- data[j,"Precision"]
    }
    
    #Plot data from table
    lines(data[,"Recall"],data[,"Precision"],lwd=width,col=colorsList[i])
    
    #splice <- data[,11:12]
    splice <- data[,which(colnames(data)=="Precision"):which(colnames(data)=="Recall")]
    #splice <- data[,7:8]
    uSplice <- unique(splice)
    
    #Calculate AUC, then add to legends collections
    legendAUC <- append(legendAUC,format(round(mean(uSplice[,1]),decimalPlaces) , nsmall=decimalPlaces))
    legendLabels <- append(legendLabels,paste("Fold",i,"(AUC =",legendAUC[i],")"))
  }
  
  #Adds control AUC to legend list, the format function is there to round off decimal
  #legendLabels <- append(legendLabels,paste("Control (AUC =",format(round(control,decimalPlaces) , nsmall=decimalPlaces),")"))
  
  #Adds legend
  legend("topright",legendLabels,lty=1,lwd=width, seg.len = 4,col = append(colorsList[1:length(files)],c("#000000")))
  
}

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
  
  plot(den1,type="l",lwd=w,xlim=c(0,1),ylim=c(0,8),xlab="Area Under the Curve",ylab="Density",main=graphName)
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




