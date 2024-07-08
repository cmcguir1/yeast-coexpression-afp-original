data <- read.csv("C:\\Users\\colem\\SummerResearch2022\\AnnoRankData.csv")

plotDist <- function(labels,model,col,add=F,scale=F,xMin=0.8) {
  
  data_vec <- data[data$Anno %in% labels & !is.na(data[[model]]),][[model]]
  den <- density(data_vec,bw=0.05)
  
  if(scale) {
    len <- nrow(data[!is.na(data[[model]]),])
    numAnnos <- length(data_vec)
    sc <- numAnnos/len
    yMax <- 1
  } else {
    sc <- 1
    yMax <- 5
    
  }
  
  
  if(!add) {
    if(scale) title <- paste(model,"Annotation Distribution (Scaled)")
    else title <- paste(model,"Annotation Distribution")
    plot(den$x,den$y*sc,type='l',lwd=5,xlim=c(xMin,1),ylim=c(0,yMax),xlab="Rank\n(0 = low confidence; 1 = high confidence)",ylab="Density")
  }
  
  a_col <- adjustcolor(col,alpha.f=0.2)
  polygon(den$x,den$y*sc,col=a_col,border=col,lwd=5)
}

colorsList <- c("#FC0303","#14A63B","#5D87F0","#7713BA","#FAEF16","#E09704")

purple <- "#7713BA"
green <- "#14A63B"
blue <- "#5D87F0"

pdf("FalseNegatives.pdf",height=6,width=10)
plotDist(c("-/+"),"NN",purple,scale=F,xMin=0)
plotDist(c("-/+"),"MEFIT",green,scale=F,add=T,xMin=0)
plotDist(c("-/+"),"SPELL",blue,scale=F,add=T,xMin=0)
legend("topleft",legend=c("MEFIT","SPELL","Neural Net"),fill=c(green,blue,purple))

for(model in c("NN","MEFIT","SPELL","bioPIXIE")) {
  
  pdf(paste(model,"AnnotationDistribution_Scaled.pdf",sep="_"),height=12,width=10)
  
  plotDist(c("-/-"),model,lightRed,scale=T)
  plotDist(c("-/+"),model,blue,add=T,scale=T)
  plotDist(c("0/-"),model,darkRed,add=T,scale=T)
  plotDist(c("+/+"),model,lightGreen,add=T,scale=T)
  plotDist(c("0/+"),model,darkGreen,add=T,scale=T)
  plotDist(c("+/-"),model,orange,add=T,scale=T)
  #plotDist("-/0",model,pink,add=T,scale=T)
  #plotDist("0/0",model,purple,add=T)
  legend("topleft",legend=c("-/-","0/-","+/+","0/+","-/+","+/-"),fill=c(lightRed,darkRed,lightGreen,darkGreen,blue,orange))
  
  dev.off()
  
  
  pdf(paste(model,"AnnotationDistribution.pdf",sep="_"),height=6,width=10)
  
  plotDist(c("-/-"),model,lightRed)
  plotDist(c("-/+"),model,blue,add=T)
  plotDist(c("0/-"),model,darkRed,add=T)
  plotDist(c("+/+"),model,lightGreen,add=T)
  plotDist(c("0/+"),model,darkGreen,add=T)
  plotDist(c("+/-"),model,orange,add=T)
  #plotDist(c("-/0"),model,pink,add=T)
  #plotDist("0/0",model,purple,add=T)
  legend("topleft",legend=c("-/-","0/-","+/+","0/+","-/+","+/-"),fill=c(lightRed,darkRed,lightGreen,darkGreen,blue,orange))
  
  dev.off()
  
  
  pdf(paste(model,"AnnotationDistribution_Reduced.pdf",sep="_"),height=6,width=12)
  
  plotDist(c("+/+","+/-","+/0"),model,lightGreen)
  plotDist(c("+/+","-/+","0/+"),model,darkGreen,add=T)
  plotDist(c("-/-","-/+","-/0"),model,lightRed,add=T)
  plotDist(c("-/-","+/-","0/-"),model,darkRed,add=T)
  
  legend("topleft",legend=c("+/*","*/+","-/*","*/-"),fill=c(lightGreen,darkGreen,lightRed,darkRed))
  
  dev.off()
  
  
  pdf(paste(model,"AnnotationDistribution_Reduced_Scaled.pdf",sep="_"),height=6,width=12)
  
  plotDist(c("+/+","+/-","+/0"),model,lightGreen,scale=T)
  plotDist(c("+/+","-/+","0/+"),model,darkGreen,add=T,scale=T)
  plotDist(c("-/-","-/+","-/0"),model,lightRed,add=T,scale=T)
  plotDist(c("-/-","+/-","0/-"),model,darkRed,add=T,scale=T)
  
  legend("topleft",legend=c("+/*","*/+","-/*","*/-"),fill=c(lightGreen,darkGreen,lightRed,darkRed))
  
  dev.off()
  
}


