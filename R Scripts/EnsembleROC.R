
ensembleROC <- function(dataFile,graphName,modern=FALSE) {
  getAUC <- function(data){
    
    decimalPlaces <- 3
    return(format(round(mean(data[,"Recall"]),decimalPlaces) , nsmall=decimalPlaces))
  }
  if (!modern){
    pixie <- read.csv("C:\\Users\\colem\\SummerResearch2022\\Yeast Resources\\ConfusionMatrixPixie.csv")
    mefit <- read.csv("C:\\Users\\colem\\SummerResearch2022\\Yeast Resources\\ConfusionMatrixMefit.csv")
    spell <- read.csv("C:\\Users\\colem\\SummerResearch2022\\Yeast Resources\\ConfusionMatrixSpell.csv")
  } else {
    pixie <- read.csv("C:\\Users\\colem\\SummerResearch2022\\Yeast Resources\\ConfusionMatrixPixie_Modern.csv")
    mefit <- read.csv("C:\\Users\\colem\\SummerResearch2022\\Yeast Resources\\ConfusionMatrixMefit_Modern.csv")
    spell <- read.csv("C:\\Users\\colem\\SummerResearch2022\\Yeast Resources\\ConfusionMatrixSpell_Modern.csv")
  }
  nn <- read.csv(dataFile)
  
  pixie <- pixie[order(pixie[,"Confidence"],decreasing=FALSE),]
  mefit <- mefit[order(mefit[,"Confidence"],decreasing=FALSE),]
  spell <- spell[order(spell[,"Rank"],decreasing=FALSE),]
  nn <- nn[order(nn[,"Score"],decreasing = FALSE),]
  
  pixie <- dplyr::filter(pixie,Agnostic!=1)
  mefit <- dplyr::filter(mefit,Agnostic!=1)
  spell <- dplyr::filter(spell,Agnostic!=1)
  nn <- dplyr::filter(nn,Label!=0)
  
  
  w <- 4
  colorsList <- c("#FC0303","#14A63B","#5D87F0","#7713BA","#FAEF16","#E09704")
  
  plot(pixie[,"False.Positive.Rate"],pixie[,"Recall"],type="l",lwd=w,col=colorsList[1],main=graphName,xlab="False Positive Rate",ylab="Recall",ylim=c(0,1))
  
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

ensemblePR <- function(dataFile,graphName,modern=FALSE) {
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
  if(!modern) {
    pixie <- read.csv("C:\\Users\\colem\\SummerResearch2022\\Yeast Resources\\ConfusionMatrixPixie.csv")
    mefit <- read.csv("C:\\Users\\colem\\SummerResearch2022\\Yeast Resources\\ConfusionMatrixMefit.csv")
    spell <- read.csv("C:\\Users\\colem\\SummerResearch2022\\Yeast Resources\\ConfusionMatrixSpell.csv")
  } else {
    pixie <- read.csv("C:\\Users\\colem\\SummerResearch2022\\Yeast Resources\\ConfusionMatrixPixie_Modern.csv")
    mefit <- read.csv("C:\\Users\\colem\\SummerResearch2022\\Yeast Resources\\ConfusionMatrixMefit_Modern.csv")
    spell <- read.csv("C:\\Users\\colem\\SummerResearch2022\\Yeast Resources\\ConfusionMatrixSpell_Modern.csv")
  }
  nn <- read.csv(dataFile)
  
  pixie <- pixie[order(pixie[,"Recall"],decreasing=FALSE),]
  mefit <- mefit[order(mefit[,"Recall"],decreasing=FALSE),]
  spell <- spell[order(spell[,"Recall"],decreasing=FALSE),]
  nn <- nn[order(nn[,"Recall"],decreasing = FALSE),]
  
  pixie <- dplyr::filter(pixie,Agnostic!=1)
  mefit <- dplyr::filter(mefit,Agnostic!=1)
  spell <- dplyr::filter(spell,Agnostic!=1)
  nn <- dplyr::filter(nn,Label!=0)
  
  pixie[,"Precision"] <- convexHull(pixie[,"Precision"])
  mefit[,"Precision"] <- convexHull(mefit[,"Precision"])
  spell[,"Precision"] <- convexHull(spell[,"Precision"])
  nn[,"Precision"] <- convexHull(nn[,"Precision"])
  
  w <- 4
  colorsList <- c("#FC0303","#14A63B","#5D87F0","#7713BA","#FAEF16","#E09704")
  
  plot(pixie[,"Recall"],pixie[,"Precision"],type="l",lwd=w,col=colorsList[1],main=graphName,xlab="Recall",ylab="Precision",log='x',ylim=c(0,1))
  
  lines(mefit[,"Recall"],mefit[,"Precision"],lwd=w,col=colorsList[2])
  
  lines(spell[,"Recall"],spell[,"Precision"],lwd=w,col=colorsList[3])
  
  lines(nn[,"Recall"],nn[,"Precision"],lwd=w,col=colorsList[4])
  
  #lines(c(0,1),c(0,1),lwd=w,col="#000000")
  
  
  
  
  legendLabels <- c()
  legendLabels <- append(legendLabels,paste("bioPIXIE (Avg. Prec. =",getAveragePrecision(pixie[,"Precision"]),")"))
  legendLabels <- append(legendLabels,paste("MEFIT (Avg. Prec. =",getAveragePrecision(mefit[,"Precision"]),")"))
  legendLabels <- append(legendLabels,paste("SPELL (Avg. Prec. =",getAveragePrecision(spell[,"Precision"]),")"))
  legendLabels <- append(legendLabels,paste("Neural Net (Avg. Prec. =",getAveragePrecision(nn[,"Precision"]),")"))
  
  legend("bottomleft",legendLabels,lwd=w,col=colorsList,seg.len = 4)
  
  
}

dataFile <- file.choose()
#dataFile <- "C:\\Users\\colem\\SummerResearch2022\\Yeast Resources\\Pairwise\\Spell\\Test\\Regular430_20x1_fold1_Val.csv"

graphName <- "Easy Negatives"
pdf("EnsembleComparision_EasyNegatives_ROC_Redo.pdf",width=6,height=12)
par(mfrow=c(2,1))
ensembleROC(dataFile=dataFile,graphName=graphName,modern=F)
ensemblePR(dataFile=dataFile,graphName=graphName,modern=F)
dev.off()



