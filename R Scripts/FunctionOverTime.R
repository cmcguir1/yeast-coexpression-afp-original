library(hash)

names <- read.csv("C:\\Users\\colem\\SummerResearch2022\\src\\PairwiseYeastNetwork\\TermNameDict.csv")
nameMap <- hash()

for(i in 1:nrow(names)){
  nameMap[[names[i,1]]] <- names[i,2]
}

terms <-read.csv("C:\\Users\\colem\\SummerResearch2022\\src\\PairwiseYeastNetwork\\SlimTerms_2007.csv")
signifcant <- 0
num <- 0

pdf("AllTerms_FuncOverTime.pdf",height=58*4,width=6)
par(mfrow=c(60,1))
for (term in terms$GO.Term){


  data <- read.csv(paste("C:\\Users\\colem\\SummerResearch2022\\Yeast Resources\\GO_Data\\Stats\\AllTerms\\",substring(term,1,2),substring(term,4,11),"_Annotations_Reduced.csv",sep=""))
  
  
  model <- "Score"
  #data <- na.omit(data)
  newFuncData <- data[data$New.Function. == 1,][[model]]
  wrongFuncData <- data[data$Wrong.Function. == 1,][[model]]
  if(NROW(newFuncData) > 1 & NROW(wrongFuncData) > 1){
    num <- num + 1
    newFunc <- density(newFuncData,adjust=0.3)
    
    wrongFunc <- density(wrongFuncData,adjust=0.3)
    plot(newFunc,xlim=c(min(min(newFunc$x),min(wrongFunc$x)),max(max(newFunc$x),max(wrongFunc$x))),ylim=c(0,max(max(newFunc$y),(max(wrongFunc$y)))),col=rgb(1,0,0),lwd=5,ylab="Density",xlab="Gene Rank",main=paste(term,nameMap[[term]],sep="\n"))
    lines(wrongFunc,col=rgb(0,1,0),lwd=5)
    ks <- ks.test(newFuncData,wrongFuncData,alternative ="greater")
    legend("topleft",legend=c(paste("New Function (",NROW(newFuncData)," genes)",sep=""),paste("Wrong Function (",NROW(wrongFuncData)," genes)",sep=""),paste("KS Test (greater) p-value:",ks$p.value)),fill=c(rgb(1,0,0),rgb(0,1,0),rgb(1,1,1)))
    if(ks$p.value < 0.05) signifcant <- signifcant + 1
    
  }
}
dev.off()
print(num)
print(signifcant)
