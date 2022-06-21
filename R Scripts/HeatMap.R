library(RColorBrewer)

plotHeatmap <- function(file,graphName){
  heatData <- read.csv(file,sep=",",row.names = 1)
  colors <- colorRampPalette(brewer.pal(9,"YlOrRd"))(100)
  cols2 <-c(colorRampPalette(c("#FFFFFF",colors[30]))(40),colorRampPalette(colors[30:100])(160))
  
  heatmap(as.matrix(heatData),Colv = NA,Rowv = NA,col=cols2,main=" ")
  legend("right",c("0.0","","","","","0.5","","","","","1.0"),col =colorRampPalette(cols2)(11),pch=15,pt.cex = 3,title="p-value")
  title(graphName,line= 3,cex.main=2)
}
file <- file.choose()

graphName <- "Brem 24 Positives"
fileName <- "Brem_24_Pos_HM.pdf"

pdf(fileName,width=12,height=8)
plotHeatmap(file=file,graphName=graphName)
dev.off()

