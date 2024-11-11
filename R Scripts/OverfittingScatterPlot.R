
file <- file.choose()
print(file)
data <- read.csv(file)
fileName <- "Batches-600000_Net-80x80x80_Overfitting_GoTermSize.pdf"
title <- "Batches 600000, Net 80x80x80"

pdf(fileName,width=8,height=8)

plot(c(0,1),c(0,1),type="l",xlim=c(0.5,1),ylim=c(0.5,1),xlab="Testing AUC",ylab="Training AUC",lwd=5,main=title)
for(i in 1:nrow(data)){
#for(i in 1:10){  
  t <- data$SG.AUC[i]
  size <- (data$SG.AUC[i] - 0.5) * 5
  #size <- data$SG.AUC[i]^2 * 2
  #size <- 2* data$Annos2007[i] / max(data$Annos2007)
  #size <- min(data$FracAnnos[i],1.5) *2
  intial <- col2rgb("yellow")
  final <-  col2rgb("blue")
  print(intial)
  print(final)
  print("-------------")
  r <- intial[1] * (1-t) + final[1] * t
  g <- intial[2] * (1-t) + final[2] * t
  b <- intial[3] * (1-t) + final[3]* t
  tcol <- rgb(r,g,b,maxColorValue = 255)
  print(tcol)
  #print(size)
  lines(data$Test.AUC[i],data$Train.AUC[i],type="p",pch=16,col="red",cex=size)
}
dev.off()





fileName <- "Batches-600000_Net-80x80x80_TestingAUC_vs_Frac-GO-Annos.pdf"
title <- "Batches 600000, Net 80x80x80"

pdf(fileName,width=8,height=8)

plot(data$Test.AUC-data$Train.AUC,data$SG.AUC,main=title,xlab="Overfitting",ylab="SG AUC",type="p",pch=16,col="red",ylim=c(0,1))
#plot(data$SG.AUC,data$Annos2007,xlim=c(0.5,1),main=title,xlab="SG AUC",ylab="Frac GO Term Annotations",type="p",pch=16,col="red")

dev.off()
