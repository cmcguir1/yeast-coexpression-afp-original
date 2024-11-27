plot(diff,termData_s$KS.CxC.CxM.Statistic)
cor.test(diff,termData_s$KS.CxC.CxM.Statistic)

plot(abs(diff),termData_s$M/termData_s$X2007.Annos,pch=16,col="black",xlab="Abs(2007 AUC - 2022 AUC)",ylab="Fraction of misannotations in 2007",xlim=c(0,0.20),ylim=c(0,1))
test <- cor.test(abs(diff),termData_s$M/termData_s$X2007.Annos)
legend("topright",legend=c(paste("r =",signif(test$estimate,digits=3)),paste("p-value =",signif(test$p.value,digits=3))))

plot(diff,termData_s$C/termData$X2022.Genes,xlim=c(-0.2,0.2),ylim=c(0,1),xlab="2007 AUC - 2022 AUC",ylab="Fraction of genes in 2022 that were annotated in 2007",pch=16,col="black")
test <- cor.test(diff,termData_s$C/termData$X2022.Genes)
legend("topright",legend=c(paste("r =",signif(test$estimate,digits=3)),paste("p-value =",signif(test$p.value,digits=3))))

plot(diff,termData$KS.Statistic,pch=16,col="black",xlab="2007 AUC - 2022 AUC",ylab="KS Test Statistic",xlim=c(-0.2,0.2),ylim=c(0,0.5))
test <- cor.test(diff,termData$KS.Statistic)
legend("topright",legend=c(paste("r =",signif(test$estimate,digits=3)),paste("p-value =",signif(test$p.value,digits=3))))

plot(diff,termData_s$KS.CxC.CxN.Statistic,pch=16,col="black",xlab="2007 AUC - 2022 AUC",ylab="KS Test Statistic",xlim=c(-0.2,0.2),ylim=c(0,0.5))
test <- cor.test(diff,termData_s$KS.CxC.CxN.Statistic)
legend("topright",legend=c(paste("r =",signif(test$estimate,digits=3)),paste("p-value =",signif(test$p.value,digits=3))))

plot(diff,termData_s$X2007.Annos,pch=16,col="black",xlab="2007 AUC - 2022 AUC",ylab="Number of Annotations in 2007",xlim=c(-0.2,0.2),ylim=c(0,400))
plot(diff,log2(termData_s$X2007.Annos),pch=16,col="black",xlab="2007 AUC - 2022 AUC",ylab="log2(Number of Annotations in 2007)",xlim=c(-0.2,0.2))
test <- cor.test(diff,log2(termData_s$X2007.Annos))
legend("topright",legend=c(paste("r =",signif(test$estimate,digits=3)),paste("p-value =",signif(test$p.value,digits=3)))) 


# Current Analysis

plot(data$Test.AUC,termData2$KS.Statistic,xlim=c(0.5,1),ylim=c(0,1),pch=16,col="black",xlab="Test AUC",ylab="KS Test Statistic")
test <- cor.test(data$Test.AUC,termData2$KS.Statistic)
legend("topright",legend=c(paste("r =",signif(test$estimate,digits=3)),paste("p-value =",signif(test$p.value,digits=3))))

plot(overfit,termData2$KS.Statistic,xlim=c(0,0.2),ylim=c(0,1),xlab ="Overfitting (2007 AUC - 2022 AUC)",ylab="KS Test Statistic",pch=16,col="black")
badTerms <- c("GO:0043543", "GO:0032200","GO:0001403","GO:0000902","GO:0006869","GO:0007124")
filt_over <- data[data$GO.Term %in% badTerms,]
test <- cor.test(overfit,termData2$KS.Statistic)
legend("topright",legend=c(paste("r =",signif(test$estimate,digits=3)),paste("p-value =",signif(test$p.value,digits=3))))


badTerms <- c("GO:0048284","GO:0043543","GO:0006470","GO:0051052","GO:0007124","GO:0032200")
goodTerms <- c("GO:0042274","GO:0000054","GO:0006364","GO:0042255","GO:0042273","GO:0032196")
#
plot(data$Test.AUC,termData$KS.Statistic,xlim=c(0.5,1),ylim=c(0,1),xlab="Testing AUC",ylab="KS Test Statistic",pch=16,col="black")
lines(data[data$GO.Term %in% badTerms,]$Test.AUC,data[data$GO.Term %in% badTerms,]$KS.Stat,pch=16,col="red",type="p")
lines(data[data$GO.Term %in% goodTerms,]$Test.AUC,data[data$GO.Term %in% goodTerms,]$KS.Stat,pch=16,col="green",type="p")
test <- cor.test(data$Test.AUC,termData$KS.Statistic)
legend("topleft",legend=c(paste("r =",signif(test$estimate,digits=3)),paste("p-value =",signif(test$p.value,digits=3))))

plot(overfitting,termData$KS.Statistic,ylim=c(0,1),xlab="Overfitting (Traing AUC - Testing AUC)",ylab="KS Test Statistic",pch=16,col="black",xlim=c(0,0.25))
lines(data[data$GO.Term %in% badTerms,]$Train.AUC-data[data$GO.Term %in% badTerms,]$Test.AUC,data[data$GO.Term %in% badTerms,]$KS.Stat,pch=16,col="red",type="p")
lines(data[data$GO.Term %in% goodTerms,]$Train.AUC-data[data$GO.Term %in% goodTerms,]$Test.AUC,data[data$GO.Term %in% goodTerms,]$KS.Stat,pch=16,col="green",type="p")
test <- cor.test(overfitting,termData$KS.Statistic)
legend("topright",legend=c(paste("r =",signif(test$estimate,digits=3)),paste("p-value =",signif(test$p.value,digits=3))))



