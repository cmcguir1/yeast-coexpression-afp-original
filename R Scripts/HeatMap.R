plotHeatmap <- function(file){
  
}
file <- file.choose()
heatData <- read.csv(file,sep=",",row.names = 1)
#heatmap(as.matrix(heatData),Colv = NA,Rowv = NA)
heatmap(as.matrix(heatData))