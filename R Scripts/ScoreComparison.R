library(stringr)
library(hash)

blue <-rgb(107, 178, 255,maxColorValue=255,alpha=64)
green <-rgb(54, 173, 100,maxColorValue=255,alpha=164)
red <- rgb(255, 110, 110,maxColorValue=255,alpha=64)

blue_border <-rgb(107, 178, 255,maxColorValue=255,alpha=255)
green_border <- rgb(54, 173, 100,maxColorValue=255,alpha=255)
red_border <- rgb(255, 110, 110,maxColorValue=255,alpha=255)


plotDist <- function(posScores,negScores,type,title="",scaleTo="none") {
  if(type == "pairwise") {
    legend <- c("Positive Pairs","Negative Pairs")
    xlab <- "Pairwise scores"
    #xlim <- c(-50,50)
  } else if (type == "single") {
    legend <- c("Positive genes","Negatives genes")
    xlab <- "Single Gene Scores (Pos)"
    #xlim <- c(-4000,4000)
    
  } else {
    legend <- c("Postiive genes","Negative genes")
    xlab <- "Single Gene Scores (Proportion)"
    #xlim <- c(-0.02,0.02)
  }
  
  posDen <- density(posScores)
  negDen <- density(negScores)
  
  posHist <- hist(posScores,breaks=50)
  negHist <- hist(negScores,breaks=50)
  
  lenPos <- length(posScores)
  lenNeg <- length(negScores)
  posProp <- lenPos / (lenPos + lenNeg)
  negProp <- 1 - posProp
  
  if(max(posDen$y)*posProp > max(negDen$y)*negProp | scaleTo == "pos") {
    yMax <-max(posDen$y)*posProp + (0.2 * max(posDen$y)*posProp)
  } else {
    yMax <-max(negDen$y)*negProp + (0.2 * max(negDen$y)*negProp)
  }
  ylim <- c(0,yMax)
  
  if(min(posDen$x) < min(negDen$x)) {
    xMin <- min(posDen$x)
  } else {
    xMin <- min(negDen$x)
  }
  
  if(max(posDen$x) > max(negDen$x)) {
    xMax <- max(posDen$x)
  } else {
    xMax <- max(negDen$x)
  }
  xGap <- (xMax - xMin) * 0.1
  
  
  xlim <- c(xMin - xGap, xMax + xGap)
  
  
  #plot((posDen$y*posProp)~posDen$x,xlab=xlab,type="l",lwd=5,xlim=xlim,ylim=ylim,main=title)
  #polygon((negDen$y*negProp)~negDen$x,col=red,border=red_border,lwd=5)
  #polygon((posDen$y*posProp)~posDen$x,col=green,border=green_border,lwd=5)
  
  plot(posHist,col="green")
  lines(negHist,col="red")
  
  legend("topright",legend=legend,fill=c(green_border,red_border),cex=1.2)
  
}

plotSingleDist <- function(scores,background,title="") {
  
  lg <- rgb(71, 230, 132,maxColorValue=255,alpha=164)
  lg_border <- rgb(71, 230, 132,maxColorValue=255,alpha=255)
  dg <- rgb(17, 140, 64,maxColorValue=255,alpha=164)
  dg_border <- rgb(17, 140, 64,maxColorValue=255,alpha=255)
  lr <- rgb(255, 110, 110,maxColorValue=255,alpha=64)
  lr_border <- rgb(255, 110, 110,maxColorValue=255,alpha=255)
  dr <- rgb(191, 17, 17,maxColorValue=255,alpha=64)
  dr_border <- rgb(191, 17, 17,maxColorValue=255,alpha=255)
  b <-rgb(42, 142, 250,maxColorValue=255,alpha=64)
  b_border <-rgb(42, 142, 250,maxColorValue=255,alpha=255)
  
  
  
  #posScores <- density(scores[scores$Label == 1,]$Score)
  #negScores <- density(scores[scores$Label == -1,]$Score)
  #posBack <- density(background[background$Label == 1,]$Score)
  #negBack <- density(background[background$Label == -1,]$Score)
  #back <- density(background$Score)
  
  posScores <- hist(scores[scores$Label == 1,]$Score,breaks=50)
  negScores <- density(scores[scores$Label == -1,]$Score)
  posBack <- density(background[background$Label == 1,]$Score)
  negBack <- density(background[background$Label == -1,]$Score)
  back <- density(background$Score)
  
  xlim <- c(min(c(posScores$x,negScores$x,back$x)),max(c(posScores$x,negScores$x,back$x)))
  ylim <- c(0,max(c(posScores$y,negScores$y,back$y,posBack$y),negBack$y))
  
  plot(posScores,xlab="Score",type="l",lwd=5,xlim=xlim,ylim=ylim,main=title)
  polygon(posScores,col=lg,border=lg_border,lwd=5)
  polygon(negScores,col=lr,border=lr_border,lwd=5)
  polygon(posBack,col=dg,border=dg_border,lwd=5)
  polygon(negBack,col=dr,border=dr_border,lwd=5)
  #polygon(back,col=b,border=b_border,lwd=5)
  
  #leg <- c("Positives to Positives","Positives to Background","Negatives to Positives","Negatives to Background","All Genes to Background")
  #legend("topright",legend=leg,fill = c(lg_border,dg_border,lr_border,dr_border,b_border),cex=1)
  
  leg <- c("Positives to Positives","Positives to Background","Negatives to Positives","Negatives to Background")
  legend("topright",legend=leg,fill = c(lg_border,dg_border,lr_border,dr_border),cex=1)
  
}


#mitoScores <- read.csv("D:/Background/SingleScores_Pos/GO-0007005_single_pos.csv")
#mitoPos <- mitoScores[mitoScores$Label == 1,]
#mitoNeg <- mitoScores[mitoScores$Label == -1,]
#plotMito <- function(scores) {
#  termPos <- scores[scores$Label == 1,]$Score
#  termNeg <- scores[scores$Label == -1,]$Score
  
#}


names <- read.csv("C:\\Users\\colem\\SummerResearch2022\\src\\PairwiseYeastNetwork\\TermNameDict.csv")
nameMap <- hash()
for(i in 1:nrow(names)){
  nameMap[[str_replace(names[i,1],":","-")]] <- names[i,2]
}

GoTerms <- read.csv("C:\\Users\\colem\\SummerResearch2022\\src\\PairwiseYeastNetwork\\GOTermIndexDictionary.csv")

getName <- function(t) {
  name <- names[names$Term == t]$Term.Name
  return(name)
}

# Triple histogram plot
for(term in GoTerms$GO.Term[7:92]){
  
  term <- str_replace(term,":","-")
  
  saveDir <- "D:/Background/ScoreGraphs_Proportional/"
  if(!dir.exists(saveDir)) {
    dir.create(saveDir)
  }
  
  pdf(paste(saveDir,term,"_ScoreDist_PosScale.pdf",sep=""),width=14,height=10)
  par(mfrow=c(1,3))
  par(cex.main=1.5)
  
  pairs <- read.csv(paste("D:/Background/PairScores/",term,"_pairs.csv",sep=""))
  plotDist(pairs[pairs$Label == 1,]$Score,pairs[pairs$Label == -1,]$Score,type="pairwise",scaleTo = "pos")
  
  single <- read.csv(paste("D:/Background/SingleScores_Pos/",term,"_single_pos.csv",sep=""))
  plotDist(single[single$Label == 1,]$Score,single[single$Label == -1,]$Score,type="single",title=paste(term,"\n",nameMap[[term]],sep=""),scaleTo = "pos")
  
  single_prop <- read.csv(paste("D:/Background/SingleScores_Prop/",term,"_single_proportion.csv",sep=""))
  plotDist(single_prop[single_prop$Label == 1,]$Score,single_prop[single_prop$Label == -1,]$Score,type="single_prop",scaleTo = "pos")
  dev.off()
  
  rm(pairs)
  rm(single)
  rm(single_prop)
  
}

# Single Histogram plot
for(term in GoTerms$GO.Term){
  
  term <- str_replace(term,":","-")
  pdf(paste("D:/Background/ScoreGraphs/",term,"_ScoreDist_Background.pdf",sep=""),width=10,height=5)
  par(cex.main=1.5)
  
  scores <- read.csv(paste("D:/Background/SingleScores_Pos/",term,"_single_pos.csv",sep=""))
  background <- read.csv(paste("D:/Background/SingleScores_Background/",term,"_single_background.csv",sep=""))
  plotSingleDist(scores,background,title=paste(term,"\n",nameMap[[term]],sep=""))
  
  dev.off()
  
  
}


# Mito Organization Comparison
for(term in GoTerms$GO.Term){
  scores <- read.csv(paste("D:/Background/SingleScores_Pos/",term,"_single_pos.csv",sep=""))
}

for(term in GoTerms$GO.Term){
  term <- str_replace(term,":","-")
  
  saveDir <- "D:/ST_AG_Comparison/"
  if(!dir.exists(saveDir)) {
    dir.create(saveDir)
  }
  
  
  
  AGSingleFile <- paste("D:/Background/SingleScores_Pos/",term,"_single_pos.csv",sep="")
  STSingleFile <- paste("C:\\Users\\colem\\SummerResearch2022\\Yeast Resources\\GraphResults\\AllSingle_New\\",gsub('-','',term),"_SingleGeneRanking.csv",sep="")
  AGPairsFile <- paste("D:/OnlyPos/PairScores/",term,"_pairs.csv",sep="")
  STPairsFile <- paste("C:\\Users\\colem\\SummerResearch2022\\Yeast Resources\\GraphResults\\AllSingle_New\\",gsub('-','',term),"_PosPairs_Combined.csv",sep="")
  
  if(file.exists(AGSingleFile) & file.exists(STSingleFile) * file.exists(AGPairsFile) & file.exists(STPairsFile)){
    AGSingle <- read.csv(AGSingleFile)
    STSingle <- read.csv(STSingleFile)
    AGPairs <- read.csv(AGPairsFile)
    STPairs <- read.csv(STPairsFile)
    
    pdf(paste(saveDir,term,"_ST_AG_Comparison.pdf"),height=8,15)
    par(mfrow=c(2,4))
    par(cex.main=1.5)
    
    plotDist(AGPairs[AGPairs$Label == 1,]$Score,AGPairs[AGPairs$Label == -1,]$Score,type="pairwise")
    plotDist(AGSingle[AGSingle$Label == 1,]$Score,AGSingle[AGSingle$Label == -1,]$Score,type="single")
    plotDist(STPairs[STPairs$Label == 1,]$Score,STPairs[STPairs$Label == -1,]$Score,type="pairwise")
    plotDist(STSingle[STSingle$X... == 1,]$Score,STSingle[STSingle$X... == -1,]$Score,type="single")
    
    plotDist(AGPairs[AGPairs$Label == 1,]$Score,AGPairs[AGPairs$Label == -1,]$Score,type="pairwise",scaleTo="pos")
    plotDist(AGSingle[AGSingle$Label == 1,]$Score,AGSingle[AGSingle$Label == -1,]$Score,type="single",scaleTo="pos")
    plotDist(STPairs[STPairs$Label == 1,]$Score,STPairs[STPairs$Label == -1,]$Score,type="pairwise",scaleTo="pos")
    plotDist(STSingle[STSingle$X... == 1,]$Score,STSingle[STSingle$X... == -1,]$Score,type="single",scaleTo="pos")
    
    mtext(paste(term,"\n",nameMap[[term]],sep=""), side = 3, line = -3, outer = TRUE)
    mtext("Single Term Network", side = 0, line = -3, outer = TRUE)
    
    
    dev.off()
  }
  
  
  
}


