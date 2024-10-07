
aucs <- read.csv(file.choose())
pcorps <- read.csv(file.choose())

#barplot(AUC~GO.Term,data=data,pch=16,vertical=TRUE,las=2,ylim=c(0,1))
main <- "SingleGene Diff. Folds"
pdf("DiffFolds_SingleGene.pdf",height=10,width=25)
par(mfrow=c(2,1),mar=c(7,5,2,2))
stripchart(AUC~GO.Term,data=aucs,pch=16,vertical=TRUE,las=2,ylim=c(0,1),main=main,ylab="AUC",xlab="",cex.axis=0.8)
mtext("GO Term",side=1,5.5)
stripchart(PCORP~GO.Term,data=pcorps,pch=16,vertical=TRUE,las=2,main="",ylab="Percent Change Over Random Precision",xlab="",cex.axis=0.8)
mtext("GO Term",side=1,5.5)
dev.off()

