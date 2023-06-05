
plotLoss <- function(data,title) {
  trainCol <- rgb(19, 87, 176,255,maxColorValue = 255)
  testCol <- rgb(130, 184, 255,255,maxColorValue=255)
  overfitCol <- rgb(130, 184, 255,64,maxColorValue=255)
  
  yMax <- max(c(data$Training.Loss,data$Testing.Loss)) * 1.2
  yMin <- min(c(data$Training.Loss,data$Testing.Loss)) * 0.8
  ylim <- c(yMin,yMax)
  
  lytickpos <- seq(yMin,yMax,10)
  
  xlim <- c(0,max(data$Batch))
  
  twoord.plot(data$Batch,data$Training.Loss,data$Batch,data$Learning.Rate,type='l',main="Loss",xlab="Number of Batches",ylab="Loss",rylab="Learning Rate",lcol=trainCol,rcol="red",lwd=5,xlim=xlim,lylim=ylim,lytickpos=lytickpos)
  lines(data$Testing.Loss~data$Batch,lwd=5,col=testCol)
  polygon(c(data$Batch,rev(data$Batch)),c(data$Testing.Loss,rev(data$Training.Loss)),border=NA,col=overfitCol)

}
data <- read.csv(file.choose())

plotLoss(data=data,title="")

fakeData <- read.csv("C:\\Users\\colem\\SummerResearch2022\\LrTestData.csv")
plotLoss(fakeData,title="")
