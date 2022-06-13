
plotCorr <- function(file) {
  
}

file <- file.choose()
table <- read.csv(file)

pos <- table[table[["Type"]] %in% c("P-P"),c("Gene.A","Gene.B","Type","Correlation")]
neg <- table[table[["Type"]] %in% c("N-N"),c("Gene.A","Gene.B","Type","Correlation")]
agn <- table[table[["Type"]] %in% c("P-N"),c("Gene.A","Gene.B","Type","Correlation")]
hist(agn[,"Correlation"])