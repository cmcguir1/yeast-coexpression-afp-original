data <- read.csv(file.choose())

blue <-rgb(40, 84, 189,maxColorValue=255,alpha=255)
plot(data$Loss~(1:nrow(data)))
