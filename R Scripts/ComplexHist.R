plotAUCDist <- function(file) {
  data <- read.csv(file)
  
  lb <-rgb(107, 178, 255,maxColorValue=255,alpha=128)
  lg <-rgb(54, 173, 100,maxColorValue=255,alpha=128)
  p <- rgb(255, 110, 110,maxColorValue=255,alpha=128)
  
  borderlb <-rgb(107, 178, 255,maxColorValue=255,alpha=255)
  borderlg <- rgb(54, 173, 100,maxColorValue=255,alpha=255)
  borderp <- rgb(255, 110, 110,maxColorValue=255,alpha=255)
  
  w <-5
  den <- density(data[,"AUC"])
  plot(den,type="l",lwd=w)
  polygon(den,col=lb,border=borderlb)
}

plotAUCDist(file.choose())