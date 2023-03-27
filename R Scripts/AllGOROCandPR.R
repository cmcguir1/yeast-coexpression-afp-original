source("C:/Users/colem/SummerResearch2022/R Scripts/ROCandPRCurves.R")
library(purrr)

scrapeGoTerms <- function(files) {
  goTerms <- c()
  for(file in files){
    relative <- substring(file,(gregexpr("/GO-",file)[[1]][1])+1,nchar(file))
    term <- substring(relative,1,(gregexpr("_",relative)[[1]][1])-1)
    goTerms <- append(term,goTerms)
    
  }
  goTerms <- unique(goTerms)
  return(goTerms)
}

find <- function(needle,haystack) {
  return(gregexpr(needle,haystack)[[1]][1])
}

rfind <- function(needle,haystack) {
  lst <- gregexpr(needle,haystack)[[1]]
  return(lst[length(lst)])
}

getStruct <- function(str) {
  rel <- substring(str,rfind("/",str),nchar(str))
  rel2 <- substring(rel,find("_",rel)+1,nchar(rel))
  struct <- substring(rel2,0,find("_",rel2)-1)
  return(struct)
}

replaceTest <- function(str) {
  testLoc <- gregexpr("_Test",str)[[1]][1]
  replaced <- paste(substring(str,0,testLoc),"Train",substring(str,testLoc+5,nchar(str)),sep="")
  return(replaced)
}


#Gets all files from Working directory
wd <- getwd()
saveDir <- "C:/Users/colem/SummerResearch2022/Yeast Resources/Yeast Graphs/LargeStruct"
#saveDir <- "D:/YeastStor/lr_decay"

dirs <- list.dirs(path = getwd(),full.names = TRUE)
dirs <- dirs[2:length(dirs)]
testDirs <- dirs[grepl("Test",dirs,fixed=TRUE)]
testDirs <- testDirs[grepl("113x5000x92",testDirs,fixed=TRUE)]
print(testDirs)


plotAll <- FALSE
desiredTerms <- c("GO-0042273","GO-0032196","GO-0009451","GO-0006897","GO-0006979","GO-0006325","GO-0000278","GO-0051321","GO-0003700","GO-0000747","GO-0006470","GO-0007033","GO-0007005")


netType <- "AllGO"
dataset <- "Original"

for(dir in testDirs) {
  setwd(dir)
  files <- list.files(full.names = TRUE,include.dirs = TRUE,path=getwd())
  setwd(saveDir)
  
  if(plotAll) terms <- scrapeGoTerms(files)
  else terms <- desiredTerms
  print(terms)
  
  struct <- getStruct(dir)
  
  testDistFiles <- files[grepl("GOTermDistribution",files,fixed=TRUE)]
  trainDistFiles <- unlist(map(testDistFiles,replaceTest))
  
  pdf(paste(netType,"_",struct,"_",dataset,"_AUCDist.pdf",sep=""),height=10,width=6)
  par(mfrow=c(2,1))
  plotAUCDist(testDistFiles,paste(netType,struct,"Testing"))
  plotAUCDist(trainDistFiles,paste(netType,struct,"Training"))
  
  dev.off()
  
  
  for(term in terms) {
    #Divides files into testing and training files
    testFiles <- files[grepl(term,files,fixed=TRUE) & grepl(struct,files,fixed=TRUE)]
    trainFiles <- unlist(map(testFiles,replaceTest))
    
    
    if(length(testFiles) == 4) {
      pdf(paste(term,"_",netType,"_",struct,"_",dataset,".pdf",sep=""),height=10,width=10)
      par(mfrow=c(2,2))
      plotROC(testFiles,paste(netType,term,struct,"Testing"))
      plotROC(trainFiles,paste(netType,term,struct,"Training"))
      plotPrecRecall(testFiles,paste(netType,term,struct,"Testing"))
      plotPrecRecall(trainFiles,paste(netType,term,struct,"Training"))
      dev.off()
    }
    
  }
}

