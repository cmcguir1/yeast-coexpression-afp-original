plotGenderTrend <- function(indata) {
  pt <- 19
  w <- 6
  plot(indata[,1], indata[,3], ylim=c(0,60),
       type = "l", col = "#498DA0", lwd = w, pch=pt,
       main = "Percentage Women",
       xlab = "Year", ylab="Percentage")
  points(indata[,1], indata[,3], col="#498DA0", pch=pt, lwd=w)
  
  lines(indata[,1], indata[,2], col="#86090f", lwd=w)
  points(indata[,1], indata[,2], col="#86090f", pch=pt, lwd=w)
  
  lines(indata[,1], indata[,4], col="#818387", lwd=w)
  points(indata[,1], indata[,4], col="#818387", pch=pt, lwd=w)
  
  legend("bottomleft", c("Trinity CSCI Degrees Conferred",
                         "Trinity Enrollment",
                         "U.S. CSI Degrees Conferred"),
         lty = 1, lwd = w, seg.len=4, pch=pt,
         col = c("#498DA0", "#86090f", "#818387"))
}

GenderOverTime <- read.delim("GenderOverTime.txt")

#pdf("GenderOverTime2.pdf", width=6, height=6)
plotGenderTrend(GenderOverTime)
#dev.off()



