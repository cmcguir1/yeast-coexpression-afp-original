



plotROC <- function(file,colorsList,graphName) {
  width = 3
  plot(file[,11], file[,10], ylim= c(0,1), type="l", col="#FC0303",
       lwd=width, main=graphName, xlab="False Positive Rate", ylab = "Recall")
  lines(c(0,1),c(0,1),lwd=width)
  
  
}

file <- read.csv("Primeg_FixedMatrix_24x20x8x1_fold1_Val.csv")


colorsList <- c("#FC0303","#B9FC44","#5D87F0","#7713BA","#FAEF16","#E09704")

plotROC(file,colorsList,"First Attempt")


