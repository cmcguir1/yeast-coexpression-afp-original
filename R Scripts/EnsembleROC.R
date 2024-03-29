lt <- 1
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
  
  plot(pixie[,"False.Positive.Rate"],pixie[,"Recall"],type="l",lwd=w,col=colorsList[1],main=graphName,xlab="False Positive Rate",ylab="Recall",ylim=c(0,1),lty=lt)
  
  lines(mefit[,"False.Positive.Rate"],mefit[,"Recall"],lwd=w,col=colorsList[2],lty=lt)
  
  lines(spell[,"False.Positive.Rate"],spell[,"Recall"],lwd=w,col=colorsList[3],lty=lt)
  
  lines(nn[,"False.Positive.Rate"],nn[,"Recall"],lwd=w,col=colorsList[4],lty=lt)
  
  lines(c(0,1),c(0,1),lwd=w,col="#000000")
  
  
  
  
  legendLabels <- c()
  legendLabels <- append(legendLabels,paste("bioPIXIE (AUC =",getAUC(pixie),")"))
  legendLabels <- append(legendLabels,paste("MEFIT (AUC =",getAUC(mefit),")"))
  legendLabels <- append(legendLabels,paste("SPELL (AUC =",getAUC(spell),")"))
  legendLabels <- append(legendLabels,paste("Neural Net (AUC =",getAUC(nn),")"))
  
  legend("bottomright",legendLabels,lwd=w,col=colorsList,seg.len = 4,lty=c(1,lt))
  
  
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
  
  plot(pixie[,"Recall"],pixie[,"Precision"],type="l",lwd=w,col=colorsList[1],main=graphName,xlab="Recall",ylab="Precision",log='x',ylim=c(0,1),lty=lt)
  
  lines(mefit[,"Recall"],mefit[,"Precision"],lwd=w,col=colorsList[2],lty=lt)
  
  lines(spell[,"Recall"],spell[,"Precision"],lwd=w,col=colorsList[3],lty=lt)
  
  lines(nn[,"Recall"],nn[,"Precision"],lwd=w,col=colorsList[4],lty=lt)
  
  #lines(c(0,1),c(0,1),lwd=w,col="#000000")
  
  
  
  
  legendLabels <- c()
  legendLabels <- append(legendLabels,paste("bioPIXIE (Avg. Prec. =",getAveragePrecision(pixie[,"Precision"]),")"))
  legendLabels <- append(legendLabels,paste("MEFIT (Avg. Prec. =",getAveragePrecision(mefit[,"Precision"]),")"))
  legendLabels <- append(legendLabels,paste("SPELL (Avg. Prec. =",getAveragePrecision(spell[,"Precision"]),")"))
  legendLabels <- append(legendLabels,paste("Neural Net (Avg. Prec. =",getAveragePrecision(nn[,"Precision"]),")"))
  
  legend("bottomleft",legendLabels,lwd=w,col=colorsList,seg.len = 4,lty=c(lt,lt))
  
  
}

createGraph <- function(dataFile,graphName,fileName,modern) {
  pdf(fileName,width=6,height=12)
  par(mfrow=c(2,1))
  ensembleROC(dataFile=dataFile,graphName=graphName,modern=modern)
  ensemblePR(dataFile=dataFile,graphName=graphName,modern=modern)
  dev.off()
}

displayGraph <- function(dataFile,graphName,fileName,modern) {
  
  ensembleROC(dataFile=dataFile,graphName=graphName,modern=modern)
  ensemblePR(dataFile=dataFile,graphName=graphName,modern=modern)
}

dataFile <- file.choose()

graphName <- ""
fileName <- "MultiTerm_Ensemble_ModernEvaluation_dashed_fixed.pdf"
modern <- T
createGraph(dataFile,graphName,fileName,modern)

displayGraph(dataFile,graphName,fileName,modern)





files <- choose.files()

nets <- c("100","200","500","500x200x100x100")
wds <- c("0.1","0.5","1")
i <- 1
for(t in 1:24) {
  
  if(t!=10) {
    if(t %% 2 == 1) {
      modern <- F
      tag <- ""
      offset <- 1
    }
    else {
      modern <- T
      tag <-"Modern"
      offset <- 0
    }
    if(t <= 8) wd <- "0.1"
    else if(t > 8 && t <= 16)wd <- "0.5"
    else wd <- "1"
    
    fileName <- paste("SingleTerm_Net_",nets[(floor(i/2)%%4)+1],"_wd_",wd,"_",tag,".pdf",sep="")
    graphTitle <- paste("Net",nets[(floor(i/2)%%4)+1],"wd",wd,tag,sep=" ")
    #print(files[i])
    createGraph(files[i],graphTitle,fileName,modern)
    
    i <- i + 1
  
  }
}

titles <- c("Net_100_wd_0.1","Net_100_wd_0.1")
fileNames <- c()



