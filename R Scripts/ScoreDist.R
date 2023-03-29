pos <- read.csv("C:\\Users\\colem\\SummerResearch2022\\posDist.csv")
neg <- read.csv("C:\\Users\\colem\\SummerResearch2022\\negDist.csv")
mix <- read.csv("C:\\Users\\colem\\SummerResearch2022\\mixDist.csv")

coAnnos <- read.csv("C:\\Users\\colem\\SummerResearch2022\\negDist_coAnno.csv")
noCoAnnos <- read.csv("C:\\Users\\colem\\SummerResearch2022\\negDist_nonCoAnno.csv")

lightBlue <-rgb(107, 178, 255,maxColorValue=255,alpha=64)
lightGreen <-rgb(54, 173, 100,maxColorValue=255,alpha=164)
pink <- rgb(255, 110, 110,maxColorValue=255,alpha=64)
purple <- rgb(120, 2, 171,maxColorValue=255,alpha=64)
white <- rgb(255, 255, 255,maxColorValue=255,alpha=64)


borderlb <-rgb(107, 178, 255,maxColorValue=255,alpha=255)
borderlg <- rgb(54, 173, 100,maxColorValue=255,alpha=255)
borderpk <- rgb(255, 110, 110,maxColorValue=255,alpha=255)
borderpurp <- rgb(120, 2, 171,maxColorValue=255,alpha=255)

plot(density(pos$Score),type="l",lwd=5)
polygon(density(pos$Score),col=lightBlue,border=borderlb,lwd=5)
polygon(density(neg$Score),col=pink,border=borderpk,lwd=5)
polygon(density(mix$Score),col=lightGreen,border=borderlg,lwd=5)

pdf("MitoScoreDist.pdf",height=8,width=10)
plot(density(noCoAnnos$Score),main="Mito Org Score Distribution",xlab="Pairwise Mito Org Scores",ylab="Density")
polygon(density(noCoAnnos$Score),col=pink,border=borderpk,lwd=5)
polygon(density(coAnnos$Score),col=lightGreen,border=borderlg,lwd=5)
polygon(density(pos$Score),col=lightBlue,border=borderlb,lwd=5)
legend("topright",legend=c("Pos Pairs","Neg Pairs (co-annotated under other terms)","Neg Pairs (no co-annotations)"),fill=c(borderlb,borderlg,borderpk))
dev.off()


