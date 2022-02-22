library(heatmap.plus)
library(gplots)
library(gtools)
library(RColorBrewer)

dpitimes=c("0.5","1","2","4","7")
dpicolbrew = brewer.pal(5,"Set1")

strains = c("4-MA15", "3-MA15g","2-MA15e","1-TOR-2","0-BatSRBD")
straincolbrew = brewer.pal(5,"Set2")


ages=c("52 weeks","20-23 weeks","<10 week")
agecolbrew = brewer.pal(3, "Set3")

legend("topleft", legend=paste(dpitimes,"dpi"), fill=dpicolbrew,cex=0.75)
legend("topright", legend=paste(strains), fill=straincolbrew,cex=0.75)
legend("bottomleft", legend=paste(ages), fill=agecolbrew,cex=0.75)