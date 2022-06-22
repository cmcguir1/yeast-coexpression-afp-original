library(RColorBrewer)

plotHeatmap <- function(file,graphName){
  heatData <- read.csv(file,sep=",",row.names = 1)
  colors <- colorRampPalette(brewer.pal(9,"YlOrRd"))(100)
  lightCols <- colorRampPalette(c("#FFFFFF",colors[1:80]))(11)
  darkCols <- colorRampPalette(colors[80:100])(90)
  cols2 <-c(lightCols,darkCols)

  heatmap(as.matrix(heatData),Colv = NA,Rowv = NA,col=cols2,main=" ")
  legend("right",c("0.00","","","","","0.05","","","","","0.10","0.10","","","","","0.50","","","","","1.00"),col=c(lightCols,colorRampPalette(colors[80:100])(11)),pch=15,pt.cex = 3,title="p-value",ncol=2)
  title(graphName,line= 2.5,cex.main=2)
}
file <- file.choose()

graphName <- "Primig Positives"
fileName <- "Primig_24_Pos_HM.pdf"

pdf(fileName,width=12,height=8)
plotHeatmap(file=file,graphName=graphName)
dev.off()

