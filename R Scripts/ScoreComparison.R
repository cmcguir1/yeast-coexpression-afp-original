library(stringr)

blue <-rgb(107, 178, 255,maxColorValue=255,alpha=64)
green <-rgb(54, 173, 100,maxColorValue=255,alpha=164)
red <- rgb(255, 110, 110,maxColorValue=255,alpha=64)

blue_border <-rgb(107, 178, 255,maxColorValue=255,alpha=255)
green_border <- rgb(54, 173, 100,maxColorValue=255,alpha=255)
red_border <- rgb(255, 110, 110,maxColorValue=255,alpha=255)


plotDist <- function(posScores,negScores,type,title="",center=FALSE) {
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
  
  if(max(posDen$y) > max(negDen$y)) {
    yMax <-max(posDen$y) + (0.2 * max(posDen$y))
  } else {
    yMax <-max(negDen$y) + (0.2 * max(negDen$y))
  }
  ylim <- c(0,yMax)
  
  if(center){
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
  }
  
  
  plot(posDen,xlab=xlab,type="l",lwd=5,xlim=xlim,ylim=ylim,main=title)
  polygon(negDen,col=red,border=red_border,lwd=5)
  polygon(posDen,col=green,border=green_border,lwd=5)
  
  legend("topright",legend=legend,fill=c(green_border,red_border),cex=1.2)
  
}


names <- read.csv("C:\\Users\\colem\\SummerResearch2022\\src\\PairwiseYeastNetwork\\TermNameDict.csv")

GoTerms <- read.csv("C:\\Users\\colem\\SummerResearch2022\\src\\PairwiseYeastNetwork\\GOTermIndexDictionary.csv")

getName <- function(t) {
  name <- names[names$Term == t]$Term.Name
  return(name)
}

for(term in GoTerms$GO.Term[1:28]){
  
  term <- str_replace(term,":","-")
 
  
  pdf(paste("D:/ScoreGraphs/",term,"_ScoreDist.pdf",sep=""),width=14,height=5)
  par(mfrow=c(1,3))
  par(cex.main=2.5)
  
  pairs <- read.csv(paste("D:/PairScores/",term,"_pairs.csv",sep=""))
  plotDist(pairs[pairs$Label == 1,]$Score,pairs[pairs$Label == -1,]$Score,type="pairwise")
  
  single <- read.csv(paste("D:/SingleScores/",term,"_single_pos.csv",sep=""))
  plotDist(single[single$Label == 1,]$Score,single[single$Label == -1,]$Score,type="single",title=term)
  
  single_prop <- read.csv(paste("D:/SingleScores_Prop/",term,"_single_proportion.csv",sep=""))
  plotDist(single_prop[single_prop$Label == 1,]$Score,single_prop[single_prop$Label == -1,]$Score,type="single_prop")
  dev.off()
  
  
  
  
  pdf(paste("D:/ScoresGraphs_centered/",term,"_ScoreDist_centered.pdf",sep=""),width=14,height=5)
  par(mfrow=c(1,3))
  par(cex.main=2.5)
  
  plotDist(pairs[pairs$Label == 1,]$Score,pairs[pairs$Label == -1,]$Score,type="pairwise")
  rm(pairs)
  
  plotDist(single[single$Label == 1,]$Score,single[single$Label == -1,]$Score,type="single",title=term)
  rm(single)
  
  plotDist(single_prop[single_prop$Label == 1,]$Score,single_prop[single_prop$Label == -1,]$Score,type="single_prop")
  rm(single_prop)
  dev.off()
}