data <- read.csv("C:\\Users\\colem\\SummerResearch2022\\src\\PairwiseYeastNetwork\\Compare\\TermAUC_Differnces.csv")
metrics <- read.csv("C:\\Users\\colem\\SummerResearch2022\\src\\PairwiseYeastNetwork\\Compare\\OverlapStats.csv")

plotDiff <- function(indep,dep,xName,yName="Overlap Score",title="") {
  plot(indep,dep,xlab=xName,ylab=yName,main=title,col="blue",pch=16)
  R <- cor(indep,dep,use="pairwise.complete.obs")
  abline(lm(dep~indep),col="red")
  if(R > 0) {
    loc <- "bottomright"
  } else {
    loc <- "topright"
  }
  
  legend(loc,legend=paste("R =",format(R,digits=4)),box.col="black")
}
pdf("OverlapAnalysis.pdf",height=16,width=8)
par(mfrow=c(4,2))
plotDiff(data$AUC.Diff,metrics$Abs.Sum,"AUC Difference",title="p value absolute sum")
plotDiff(data$Avg.Prec.Diff,metrics$Abs.Sum,"Avg Prec Difference",title="p value absolute sum")

plotDiff(data$AUC.Diff,metrics$Sig.Sum,"AUC Difference",title="p value sigmoidal sum")
plotDiff(data$Avg.Prec.Diff,metrics$Sig.Sum,"Avg Prec Difference",title="p value sigmoidal sum")

plotDiff(data$AUC.Diff,metrics$Inverse.Sum,"AUC Difference",title="p value inverse sigmoidal sum")
plotDiff(data$Avg.Prec.Diff,metrics$Inverse.Sum,"Avg Prec Difference",title="p value inverse sigmoidal sum")

plotDiff(data$AUC.Diff,metrics$Dis.Total.3,"AUC Difference",title="p value discrete total (p < 0.01)")
plotDiff(data$Avg.Prec.Diff,metrics$Dis.Total.3,"Avg Prec Difference",title="p value discrete total (p < 0.01)")
dev.off()




