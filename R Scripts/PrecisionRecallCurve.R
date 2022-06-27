
plotPrecRecall <- function(files,colorsList,graphName) {
  width = 4
  decimalPlaces = 3
  
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
  
  splice <- data[,11:12]
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
    
    splice <- data[,11:12]
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
#Read in multiple files
files = choose.files(default=paste0(getwd(),"/*.*"))

colorsList <- c("#FC0303","#14A63B","#5D87F0","#7713BA","#FAEF16","#E09704")

graphName <- "SPELL Network 430 Dataset: 430x20x10x1 Batch 50 Validation"


pdf("SPELL_430_430x20x10x1_batch50_Val_PR.pdf",width=8,height=6)
plotPrecRecall(files=files,colorsList=colorsList,graphName=graphName)
dev.off()
