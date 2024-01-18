source("C:/Users/colem/SummerResearch2022/R Scripts/StringFunctions.R")
library(stringr)
library(hash)

ROC <- function(dataFile,graphName) {
  getAUC <- function(data){
    decimalPlaces <- 3
    return(format(round(mean(data[,"Recall"]),decimalPlaces) , nsmall=decimalPlaces))
  }
  
  nn <- read.csv(dataFile)
  
  nn <- nn[order(nn[,"Score"],decreasing = FALSE),]
  
  nn <- dplyr::filter(nn,Label!=0)
  
  w <- 4
  colorsList <- c("#FC0303","#14A63B","#5D87F0","#7713BA","#FAEF16","#E09704")
  
  plot(nn[,"False.Positive.Rate"],nn[,"Recall"],type="l",lwd=w,col=colorsList[1],main=graphName,xlab="False Positive Rate",ylab="Recall")
  
  
  lines(c(0,1),c(0,1),lwd=w,col="#000000")
  
  legendLabels <- c()
  legendLabels <- append(legendLabels,paste("Neural Net (AUC =",getAUC(nn),")"))
  
  legend("bottomright",legendLabels,lwd=w,col=colorsList,seg.len = 4)
  
  
}

PR <- function(dataFile,graphName) {
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
  
  nn <- read.csv(dataFile)
  
  nn <- nn[order(nn[,"Recall"],decreasing = FALSE),]
  nn <- dplyr::filter(nn,Label!=0)
  prec_ch <- convexHull(nn[,"Precision"])
  
  w <- 4
  colorsList <- c("#FC0303","#14A63B","#5D87F0","#7713BA","#FAEF16","#E09704")
  
  plot(nn[,"Recall"],prec_ch,type="l",lwd=w,col=colorsList[1],main=graphName,xlab="Recall",ylab="Precision",ylim=c(0,1),log='x')
  
  
  legendLabels <- c()
  legendLabels <- append(legendLabels,paste("Average Precision =",getAveragePrecision(prec_ch),")"))
  
  legend("bottomright",legendLabels,lwd=w,col=colorsList,seg.len = 4)
  
  
}

wd <- getwd()
name <- "bioPIXIE_CE_20"
saveDir <- "D:/Optimization_Redo/ROC_Summary"
if(!dir.exists(saveDir)) dir.create(saveDir)
files <- list.files(full.names = TRUE,include.dirs = TRUE,path=getwd())
stub <- substring(files[1],1,rfind("_",files[1]))

#Scans list of files and makes a vector all GO terms that appear in files names
goTerms <- c()
for(file in files){
  relative <- substring(file,(gregexpr("_GO",file)[[1]][1])+1,nchar(file))
  term <- substring(relative,1,(gregexpr(".csv",relative)[[1]][1])-1)
  if(nchar(term) <= 9) goTerms <- c(goTerms,term)
}

#Makes a dictionary mapping GO term numbers to GO term names
names <- read.csv("C:\\Users\\colem\\SummerResearch2022\\src\\PairwiseYeastNetwork\\TermNameDict.csv")
nameMap <- hash()
for(i in 1:nrow(names)){
  nameMap[[str_replace(names[i,1],":","")]] <- names[i,2]
}

setwd(saveDir)
pdf(paste(name,"_ROC_Summary.pdf",sep=""),height=50,width=20)
par(mfrow=c(11,5))
for(term in goTerms){
   ROC(paste(stub,term,".csv",sep=""),paste(term,"\n",nameMap[[term]]))
}
dev.off()

pdf(paste(name,"_PR_Summary.pdf",sep=""),height=50,width=20)
par(mfrow=c(11,5))
for(term in goTerms){
  PR(paste(stub,term,".csv",sep=""),paste(term,"\n",nameMap[[term]]))
}
dev.off()

