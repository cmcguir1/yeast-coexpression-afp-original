source("C:/Users/colem/SummerResearch2022/R Scripts/ROCandPRCurves.R")

#Temporarily suppressed global warnings
#options(warn=-1)

#Gets all files from Working directory
wd <- getwd()
files <- list.files(full.names = TRUE,include.dirs = TRUE,path=getwd())
print(files)

#Scans list of files and makes a vector all GO terms that appear in files names
goTerms <- c()
for(file in files){
  relative <- substring(file,(gregexpr("/GO",file)[[1]][1])+1,nchar(file))
  term <- substring(relative,1,(gregexpr("_",relative)[[1]][1])-1)
  goTerms <- append(term,goTerms)
  
}
goTerms <- unique(goTerms)
print(goTerms)


structures <- c("d0_wd0","d0.1_wd0","d0.5_wd0",
                "d0_wd0.01","d0.1_wd0.01","d0.5_wd0.01",
                "d0_wd0.001","d0.1_wd0.001","d0.5_wd0.001",
                "d0_wd0.0001","d0.1_wd0.0001","d0.5_wd0.0001") #List of structures that the scripts will make graphs for

type <- "ST" #Type specifies whether the modern or original microarray assay datasets were used

setwd("D:/Paper/SingleTerm_PS/")

#Loops over all structures and GO terms
for(struct in structures){
  for(term in goTerms) {
    #Divides files into testing and training files
    termFiles <- files[grepl(term,files,fixed=TRUE) & grepl(struct,files,fixed=TRUE)]
    testFiles <- termFiles[grepl("Val",termFiles,fixed=TRUE)]
    trainFiles <- termFiles[grepl("Train",termFiles,fixed=TRUE)]
    
    #if 
    if(length(testFiles) == 4 & length(trainFiles) == 4) {
      print("Making Graph")
      modTerm <- paste(substring(term,1,2),"-",substring(term,3,nchar(term)))
      pdf(file=paste(term,"_SingleTerm_",struct,"_",type,".pdf",sep=""),height=10,width=10)
      par(mfrow=c(2,2))
      plotROC(testFiles,paste("SingleTerm",modTerm,struct,"Testing"))
      plotROC(trainFiles,paste("SingleTerm",modTerm,struct,"Training"))
      plotPrecRecall(testFiles,paste("SingleTerm",modTerm,struct,"Testing"))
      plotPrecRecall(trainFiles,paste("SingleTerm",modTerm,struct,"Training"))
      dev.off()
    }
  }
}
#options(warn=0)
setwd(wd)
