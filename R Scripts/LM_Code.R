### Script to create scatterplot with regression line

# load your data
# Data = Dye (or whatever you named it)
#Import data set

#This code allows you to go searching for your data set on your computer
DyeData<-read.csv(file.choose(), header = T, stringsAsFactors = T)

# If you did not follow the script on line 8, but renamed your data set something other than "DyeData", 
# be sure to change all the following DyeData to whatever you named your data!

#Plot your data
plot(DyeData$conc, DyeData$abs, xlab = "Concentration", ylab = "Absorbance")

#Conduct a linear regression to get your regression line
dye<-lm(abs~conc, data = DyeData)

#inspect the regression outcome to get your R-squared value
summary(dye)

#Add your line regression line to your plot
abline(dye)

#Add your R-squared value to your plot
legend("topleft",legend=paste("R2 is", format(summary(dye)$r.squared,digits=3)))
