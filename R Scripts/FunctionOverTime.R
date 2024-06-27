data <- read.csv(file.choose())

model <- "MEFIT"
data <- na.omit(data)
newFunc <- density(data[data$NewFunc == 1 & data$MEFIT != "NA",][[model]],adjust=0.3)
wrongFunc <- density(data[data$WrongFunc == 1,][[model]],adjust=0.3)
plot(newFunc,ylim=c(0,8),col=rgb(1,0,0),lwd=5,ylab="Density",xlab="Gene Rank",main=paste(model,"-/+ Predictions"))
lines(wrongFunc,col=rgb(0,1,0),lwd=5)
legend("topleft",legend=c("New Function (95 genes)","Wrong Function (22 genes)"),fill=c(rgb(1,0,0),rgb(0,1,0)))
ks.test(data[data$NewFunc == 1,][[model]],data[data$WrongFunc == 1,][[model]],alternative ="greater")
