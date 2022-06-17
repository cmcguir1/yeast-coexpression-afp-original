
plotCorr <- function(file,graphName) {
  table <- read.csv(file)
  
  pos <- table[table[["Type"]] %in% c("P-P"),c("Gene.A","Gene.B","Type","Correlation")]
  neg <- table[table[["Type"]] %in% c("N-N"),c("Gene.A","Gene.B","Type","Correlation")]
  agn <- table[table[["Type"]] %in% c("P-N"),c("Gene.A","Gene.B","Type","Correlation")]
  
  lb <-rgb(107, 178, 255,maxColorValue=255,alpha=128)
  lg <-rgb(54, 173, 100,maxColorValue=255,alpha=128)
  p <- rgb(255, 110, 110,maxColorValue=255,alpha=128)
  
  legendlb <-rgb(107, 178, 255,maxColorValue=255,alpha=255)
  legendlg <- rgb(54, 173, 100,maxColorValue=255,alpha=255)
  legendp <- rgb(255, 110, 110,maxColorValue=255,alpha=255)
  
  numBreaks <- 24
  
  w <- 5
  d1 <- density(agn[,"Correlation"],adjust=0.75)
  d2 <- density(neg[,"Correlation"],adjust=0.75)
  d3 <- density(pos[,"Correlation"],adjust=0.75)
  
  plot(d1,type='l',col=legendp,lwd=w,xlim=c(-1,1),ylim=c(0,3),main=graphName,xlab="Pearson Correlation",ylab="Density")
  lines(d2,type='l',col=legendlb,lwd=w)
  lines(d3,type='l',col=legendlg,lwd=w)
  polygon(d1,col=p,border=legendp)
  polygon(d2,col=lb,border=legendlb)
  polygon(d3,col=lg,border=legendlg)
  
  legend("topright",c("Positive Pairs","Negative Pairs","Agnositc Pairs"),pch=15,col = c(legendlg,legendp,legendlb),pt.cex = 2)
}

file <- file.choose()

fileName = "Syn_Med_36-264_1_CorrelationDist.pdf"
graphName = "Synthetic Medium 36-264 Dataset 1"

pdf(fileName,width=8,height=6)
plotCorr(file = file,graphName=graphName)
dev.off()


#plot(h1$mids, h1$density,type='l',col=legendp,lwd=w,xlim=c(-1,1),ylim=c(0,3),main=graphName,xlab="Pearson Correlation",ylab="Density")
#lines(h2$mids, h2$density,type='l',col=legendlb,lwd=w)
#lines(h3$mids, h3$density,type='l',col=legendlg,lwd=w)

#h1 <- hist(agn[,"Correlation"],col=p,breaks=numBreaks,xlim=c(-1,1),ylim=c(0,2),xlab="Pearson Correlation",ylab="Percentage",main=graphName,freq = FALSE)
#h2 <- hist(neg[,"Correlation"],col=lb,add=TRUE,breaks=numBreaks,freq=FALSE)
#h3 <- hist(pos[,"Correlation"],col=lg,add=TRUE,breaks=numBreaks,freq=FALSE)


