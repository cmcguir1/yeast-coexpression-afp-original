data <- read.csv("C:\\Users\\colem\\SummerResearch2022\\src\\PairwiseYeastNetwork\\Compare\\TermAUC_Differnces.csv")
metrics <- 
plot(data$AUC.Diff,data$Avg.Prec.Diff)
