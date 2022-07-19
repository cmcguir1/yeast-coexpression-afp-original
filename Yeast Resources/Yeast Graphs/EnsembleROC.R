getAUC <- function(data){
  decimalPlaces <- 3
  return(format(round(mean(data[,"Recall"]),decimalPlaces) , nsmall=decimalPlaces))
}

ensembleROC <- function(dataFile,graphName) {
  pixie <- read.csv("C:\\Users\\colem\\SummerResearch2022\\Yeast Resources\\ConfusionMatrixPixie.csv")
  mefit <- read.csv("C:\\Users\\colem\\SummerResearch2022\\Yeast Resources\\ConfusionMatrixMefit.csv")
  spell <- read.csv("C:\\Users\\colem\\SummerResearch2022\\Yeast Resources\\ConfusionMatrixSpell.csv")
  nn <- read.csv(dataFile)
  
  pixie <- pixie[order(pixie[,"Confidence"],decreasing=FALSE),]
  mefit <- mefit[order(mefit[,"Confidence"],decreasing=FALSE),]
  spell <- spell[order(spell[,"Rank"],decreasing=FALSE),]
  nn <- nn[order(nn[,"Score"],decreasing = FALSE),]
  
  w <- 4
  colorsList <- c("#FC0303","#14A63B","#5D87F0","#7713BA","#FAEF16","#E09704")
  
  plot(pixie[,"False.Positive.Rate"],pixie[,"Recall"],type="l",lwd=w,col=colorsList[1],main=graphName,xlab="False Positive Rate",ylab="Recall")
  
  lines(mefit[,"False.Positive.Rate"],mefit[,"Recall"],lwd=w,col=colorsList[2])
  
  lines(spell[,"False.Positive.Rate"],spell[,"Recall"],lwd=w,col=colorsList[3])
  
  lines(nn[,"False.Positive.Rate"],nn[,"Recall"],lwd=w,col=colorsList[4])
  
  lines(c(0,1),c(0,1),lwd=w,col="#000000")
  
  legendLabels <- c()
  legendLabels <- append(legendLabels,paste("bioPIXIE (AUC =",getAUC(pixie),")"))
  legendLabels <- append(legendLabels,paste("MEFIT (AUC =",getAUC(mefit),")"))
  legendLabels <- append(legendLabels,paste("SPELL (AUC =",getAUC(spell),")"))
  legendLabels <- append(legendLabels,paste("Neural Net (AUC =",getAUC(nn),")"))
  
  legend("bottomright",legendLabels,lwd=w,col=colorsList,seg.len = 4)
  
  
}

dataFile <- file.choose()
#dataFile <- "C:\\Users\\colem\\SummerResearch2022\\Yeast Resources\\Pairwise\\Spell\\Test\\Regular430_20x1_fold1_Val.csv"
graphName <- "Ensemble Comparison 113x20x1"
pdf("EnsembleComparision_HalfPos_113x20x1_ROC.pdf",width=6,height=6)
ensembleROC(dataFile=dataFile,graphName=graphName)
dev.off()
