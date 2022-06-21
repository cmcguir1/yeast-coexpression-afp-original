
plotROC <- function(files,colorsList,graphName) {
  width = 4
  decimalPlaces = 3
  
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
#Read in multiple files
files = choose.files(default=paste0(getwd(),"/*.*"))

colorsList <- c("#FC0303","#14A63B","#5D87F0","#7713BA","#FAEF16","#E09704")

graphName <- "SPELL Network 50 Dataset: 50x20x1 Validation"


#pell_50_50x20x1_Val_ROC.pdf",width=6,height=6)
plotROC(files=files,colorsList=colorsList,graphName=graphName)
#dev.off()


