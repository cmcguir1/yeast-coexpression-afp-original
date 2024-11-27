map <- function(x,xMin,xMax,yMin,yMax) {
  frac <- (x-xMin)/(xMax-xMin)
  y <- frac*(yMax-yMin) + yMin
  return(y)
}

# Obtains overfitting data, which contains data about the number of annotations for each GO term
file <- "C:\\Users\\colem\\SummerResearch2022\\Yeast Resources\\Pairwise\\Spell\\OverfittingTest\\Batches_600000_x_b_113x80x80x80x79_lr0.01_batch50_lfBCE_OverfittingAssessment.csv"
data <- read.csv(file)
ofdata <- data[data[[1]] %in% onto2007f[[1]],]

termData <- read.csv(file.choose())

intial <- c(212, 216, 252)
final <-  c(0, 10, 102)
i_col <- rgb(intial[1],intial[2],intial[3],maxColorValue = 255)
f_col <- rgb(final[1],final[2],final[3],maxColorValue = 255)


fileName <- "2007-GO-AUC_2007-GO-AUC(2022-eval)_size=KS-test-stat.pdf"

pdf(fileName,width=12,height=8)


# Set up layout: two panels - scatter plot and color legend
layout(matrix(c(1, 2), ncol = 2), widths = c(4, 1))
# Plot the scatter plot with colored points
par(mar = c(5, 4, 4, 2)) # Adjust margins for the scatter plot
# Plot the color gradient legend
par(mar = c(5, 2, 4, 2)) # Adjust margins for the legend


p_g2007_o2007 <- "C:\\Users\\colem\\SummerResearch2022\\Yeast Resources\\Pairwise\\Spell\\Expression_Ontology_Combinations\\Expr-2007_Onto-2007_x_b_113x80x80x80x79_lr0.01_batch50_lfBCE_OverfittingAssessment.csv"
p_g2007_o2022 <- "C:\\Users\\colem\\SummerResearch2022\\Yeast Resources\\Pairwise\\Spell\\Expression_Ontology_Combinations\\Expr-2007_Onto-2022_x_b_113x80x80x80x93_lr0.01_batch50_lfBCE_OverfittingAssessment.csv"
p_g2022_o2007 <- "C:\\Users\\colem\\SummerResearch2022\\Yeast Resources\\Pairwise\\Spell\\Expression_Ontology_Combinations\\Expr-2022_Onto-2007_x_b_430x80x80x80x79_lr0.01_batch50_lfBCE_OverfittingAssessment.csv"
p_g2022_o2022 <- "C:\\Users\\colem\\SummerResearch2022\\Yeast Resources\\Pairwise\\Spell\\Expression_Ontology_Combinations\\Expr-2022_Onto-2022_x_b_430x80x80x80x93_lr0.01_batch50_lfBCE_OverfittingAssessment.csv"


g2007_o2007 <- "C:\\Users\\colem\\SummerResearch2022\\Yeast Resources\\GraphResults\\Expression_Ontology_Combinations\\_Expr-2007_Onto-2007113x80x80x80x79GOTermDistribution_2007_Trained.csv"
g2007_o2022 <- "C:\\Users\\colem\\SummerResearch2022\\Yeast Resources\\GraphResults\\Expression_Ontology_Combinations\\_Expr-2007_Onto-2022113x80x80x80x93GOTermDistribution_2022_Trained.csv"
g2022_o2007 <- "C:\\Users\\colem\\SummerResearch2022\\Yeast Resources\\GraphResults\\Expression_Ontology_Combinations\\_Expr-2022_Onto-2007430x80x80x80x79GOTermDistribution_2007_Trained.csv"
g2022_o2022 <- "C:\\Users\\colem\\SummerResearch2022\\Yeast Resources\\GraphResults\\Expression_Ontology_Combinations\\_Expr-2022_Onto-2022430x80x80x80x93GOTermDistribution_2022_Trained.csv"

g2007_o2007_e2022 <- "C:\\Users\\colem\\SummerResearch2022\\Yeast Resources\\GraphResults\\Expression_Ontology_Combinations\\_Expr-2007_Onto-2007113x80x80x80x79GOTermDistribution_2022_Eval.csv"
g2007_o2022_e2007 <- "C:\\Users\\colem\\SummerResearch2022\\Yeast Resources\\GraphResults\\Expression_Ontology_Combinations\\_Expr-2007_Onto-2022113x80x80x80x93GOTermDistribution_2007_Eval.csv"
g2022_o2007_e2022 <- "C:\\Users\\colem\\SummerResearch2022\\Yeast Resources\\GraphResults\\Expression_Ontology_Combinations\\_Expr-2022_Onto-2007430x80x80x80x79GOTermDistribution_2022_Eval.csv"
g2022_o2022_e2007 <- "C:\\Users\\colem\\SummerResearch2022\\Yeast Resources\\GraphResults\\Expression_Ontology_Combinations\\_Expr-2022_Onto-2022430x80x80x80x93GOTermDistribution_2007_Eval.csv"


c2007 <- read.csv(g2022_o2007)
#c2007 <- read.csv(g2022_o2007_e2022)
c2022 <- read.csv(g2022_o2022)


c2007 <- c2007[c2007$GO.Term %in% termData$Term,]
c2007 <- c2007[c2007$GO.Term %in% c2022$GO.Term,]
c2022 <- c2022[c2022$GO.Term %in% c2007$GO.Term,]

#fileName <- "GeneOntology_2007vs2022_Pairwise_Comparison.pdf"
#pdf(fileName,width=6,height=6)

ks <- termData$KS.Stat.2022 - termData$KS.Stat.2007


plot(c(0,1),c(0,1),type='l',xlim=c(0.5,1),ylim=c(0.5,1),xlab="2007 GO Annotations AUC",ylab="2022 GO Annotations AUC")
for(i in 1:nrow(c2007)){
  size <- 1
  
  t <- map(ks[i],min(ks),max(ks),0,1)
  size <- 1.5
  
  #if (termData$Removed[i] == 0) t <- 0
  #else t <- map(log2(termData$Removed[i]),0,max(log2(termData$Removed)),0,1)
  
  #if(termData$Difference[i] <= 0) t<- 0
  #else t <- map(log2(termData$Difference[i]),0,log2(max(termData$Difference)),0,1)
  
  
  #if(termData$Removed[i] != 0) t <- (termData$Difference[i]/termData$Removed[i]) /35
  #else t <- 1
  #print(t)
  #size <- t
  
  #
  
  #t <- map(ofdata$Annos2007[i], min(ofdata$Annos2007), max(ofdata$Annos2007),0,1)
  #size <- map(ofdata$Annos2007[i], min(ofdata$Annos2007), max(ofdata$Annos2007),1,3)
  

  
  
  r <- intial[1] * (1-t) + final[1] * t
  g <- intial[2] * (1-t) + final[2] * t
  b <- intial[3] * (1-t) + final[3]* t
  tcol <- rgb(r,g,b,maxColorValue = 255)
  #tcol <- "black"
  
  lines(c2007$AUC[i],c2022$AUC[i],type="p",pch=16,col=tcol,cex=size)
  #lines(c2007$Test.AUC[i],c2022$Test.AUC[i],type="p",pch=16,col=tcol,cex=size)
}
dev.off()

colfunc <- colorRampPalette(c(i_col,f_col)) # Interpolate between blue and red
image(
  z = matrix(seq(0, 1, length = 100), nrow = 1), 
  col = colfunc(100), 
  xaxt = "n", 
  yaxt = "n"
)
axis(4, at = seq(0, 1, by = 0.2), labels = round(seq(0.5, 1, length.out = 6), 2), las = 1)
mtext("KS Test Statistic", side = 1, line = 1)


dev.off()
