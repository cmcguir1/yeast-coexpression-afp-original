source("C:/Users/colem/SummerResearch2022/R Scripts/ROCCurve.R")

#Read in multiple files
files = choose.files(default=paste0(getwd(),"/*.*"))

name <- "Single Term GO-0006325"
struct <- "113x200x1"
type <- "Train"

graph <- paste(name,struct,type,sep=" ")
fileName <- paste(name,"_",struct,"_ROC_",type,".pdf",sep="")

currentWd = getwd()
setwd("C:/Users/colem/SummerResearch2022/Yeast Resources/Yeast Graphs/SingleTerms")
#pdf(fileName,width=6,height=6)
plotROC(files=files,graphName=graphName)
#dev.off()
setwd(currentWd)