
plotROC <- function(files,colorsList,graphName) {
  width = 4
  decimalPlaces = 3
  
  
  lg <-rgb(20, 166, 59,maxColorValue=255,alpha=128)
  grey <-rgb(0, 0, 0,maxColorValue=255,alpha=128)
  
  #Initialize lists that will store information for the legend
  legendLabels <- c()
  legendAUC <- c()
  names <- c("Excellent","Great","Good","Terrible")
  
  #Reads in the first element of the files collection
  data <- read.csv(files[2])
  #Sorts data table by the Score column in ascending order
  data <- data[order(data[,"Score"],decreasing = FALSE),]
  #Creates a plot of the first data series
  plot(data[,"False.Positive.Rate"], data[,"Recall"], ylim= c(0,1), type="l", col=colorsList[2],
       lwd=width, main=graphName, xlab="False Positive Rate", ylab = "Recall")
  polygon(data[,"False.Positive.Rate"], data[,"Recall"],col=lg,border=colorsList[2])
  polygon(c(0,1,1),c(0,1,0),col=grey,border="#000000")
  lines(c(0,1),c(0,1),col="#000000",lwd =4)
  
  #Calculates AUC for first curve, the format function rounds the AUC off at decimal Places
  legendAUC <- append(legendAUC,format(round(mean(data[,"Recall"]),decimalPlaces) , nsmall=decimalPlaces))
  legendLabels <- append(legendLabels,paste(names[1],"(AUC =",legendAUC[1],")"))
  
  
  #Adds legend
  #legend("bottomright",legendLabels,lty=1,lwd=width, seg.len = 4,col = c(colorsList[1],colorsList[2],colorsList[3],"#000000"))
  
  
}
#Read in multiple files
#files = choose.files(default=paste0(getwd(),"/*.*"))

files = c("C:\\Users\\colem\\SummerResearch2022\\Yeast Resources\\Pairwise\\Spell\\OtherGOTerms\\Meiosis_20x1_fold1_Val.csv",
          "C:\\Users\\colem\\SummerResearch2022\\Yeast Resources\\Pairwise\\Spell\\OtherGOTerms\\DNARepair_20x1_fold1_Val.csv",
          "C:\\Users\\colem\\SummerResearch2022\\Yeast Resources\\Pairwise\\Spell\\Original\\Original_100x1_Val_fold1.csv")

colorsList <- c("#FC0303","#14A63B","#5D87F0","#7713BA","#FAEF16","#E09704")

graphName <- "Example ROC Curve"


pdf("ROCExampleAUCRandom.pdf",width=6,height=6)
plotROC(files=files,colorsList=colorsList,graphName=graphName)
dev.off()


