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
saveDir <- "D:/Batch_PS/Pairwise"
if(!dir.exists(saveDir)) dir.create(saveDir)


dirs <- list.dirs(path = getwd(),full.names = TRUE)
dirs <- dirs[2:length(dirs)]
testDirs <- dirs[grepl("Test",dirs,fixed=TRUE)]
#testDirs <- testDirs[grepl("CE",testDirs,fixed=TRUE)]
#testDirs <- testDirs[grepl("Alpha_0_",testDirs,fixed=TRUE)]
print(testDirs)


plotAll <- FALSE
desiredTerms <- c("GO-0007005","GO-0042273","GO-0032196","GO-0009451","GO-0006897","GO-0006979","GO-0006325","GO-0000278","GO-0051321","GO-0003700","GO-0000747","GO-0006470","GO-0007033")
desiredTerms <- c("GO-0007005")
netTypes <- c("Folds1_batch50","Folds1_batch5000","Folds1_batch500",
              "Folds2_batch50","Folds2_batch5000","Folds2_batch500",
              "Folds3_batch50","Folds3_batch5000","Folds3_batch500",
              "Folds4_batch50","Folds4_batch5000","Folds4_batch500",
              "Folds5_batch50","Folds5_batch5000","Folds5_batch500")

dataset <- "AllGO"

if(plotAll) { terms <- scrapeGoTerms(files)
} else terms <- desiredTerms
print(terms)
terms <- append("AnyCoAnnos",terms)

i <- 1
for(dir in testDirs) {
  setwd(dir)
  files <- list.files(full.names = TRUE,include.dirs = TRUE,path=getwd())
  setwd(saveDir)
  
  
  
  struct <- getStruct(dir)
  
  testDistFiles <- files[grepl("GOTermDistribution",files,fixed=TRUE)]
  trainDistFiles <- unlist(map(testDistFiles,replaceTest))
  
  pdf(paste(netTypes[i],"_",struct,"_",dataset,"_AUCDist.pdf",sep=""),height=10,width=6)
  par(mfrow=c(2,1))
  plotAUCDist(testDistFiles,paste(netTypes[i],struct,"Testing"))
  plotAUCDist(trainDistFiles,paste(netTypes[i],struct,"Training"))
  
  dev.off()
  
  
  for(term in terms) {
    #Divides files into testing and training files
    testFiles <- files[grepl(term,files,fixed=TRUE) & grepl(struct,files,fixed=TRUE)]
    trainFiles <- unlist(map(testFiles,replaceTest))
    
    
    if(length(testFiles) == 4) {
      pdf(paste(term,"_",netTypes[i],"_",struct,"_",dataset,".pdf",sep=""),height=10,width=10)
      par(mfrow=c(2,2))
      plotROC(testFiles,paste(netTypes[i],term,struct,"Testing"))
      plotROC(trainFiles,paste(netTypes[i],term,struct,"Training"))
      plotPrecRecall(testFiles,paste(netTypes[i],term,struct,"Testing"))
      plotPrecRecall(trainFiles,paste(netTypes[i],term,struct,"Training"))
      dev.off()
    }
    
  }
  i <- i + 1
}
setwd(wd)

