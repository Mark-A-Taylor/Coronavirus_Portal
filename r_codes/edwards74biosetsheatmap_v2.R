#Mike Edwards 74 biosets heatmap

library(heatmap.plus)
library(gplots)
library(gtools)
library(RColorBrewer)

#dpitimes=c("0.5","1","2","4","7")
#dpicolbrew = brewer.pal(5,"Set1")
dpicolors <- unlist(lapply(rownames(hmdata1),function(x){
  if(grepl("867451|867454|867457|867478|867481|867484",x)) '#E41A1C' #0.5 DPI
  else if(grepl("926614|494014|494017|494020|494023|867460|867463|867466|867487|867490|867493|821644|823390|839425|839437",x)) '#377EB8' #1 DPI
  else if(grepl("926620|494026|494029|494032|494035|867469|867472|867475|867496|867499|867502|821650|823396|839428|839440|833449|1326109|957616|995281",x)) '#4DAF4A' #2 DPI
  else if(grepl("494038|494041|494044|494047|867505|867508|867511|685244|685187|685193|821656|823402|839431|839443|833452|840316|834109|957619|995284",x)) '#984EA3' #4 DPI
  else if(grepl("494050|494053|494056|494011|685247|685178|685217|821662|823408|839434|839446|833455|840319|834112|995287",x)) '#FF7F00' #7 DPI
}))

#strains = c("4-MA15", "3-MA15g","2-MA15e","1-TOR-2","0-BatSRBD")
#straincolbrew = brewer.pal(5,"Set2")
straincolors <- unlist(lapply(rownames(hmdata1),function(x){
  if(grepl("867451|867478|494014|494017|494020|494023|867460|867487|821644|823390|839437|494026|494029|494032|494035|867469|867496|821650|823396|839440|833449|1326109|957616|995281|494038|494041|494044|494047|867505|685244|685187|685193|821656|823402|839443|833452|840316|834109|957619|995284|494050|494053|494056|494011|685247|685178|685217|821662|823408|839446|833455|840319|834112|995287", x)) '#66C2A5' #4-MA15
  else if(grepl("867457|867484|867466|867493|867475|867502|867511", x)) '#Fc8D62' #3-MA15g
  else if(grepl("867454|867481|867463|867490|867472|867499|867508", x)) '#8DA0CB' #2-MA15e
  else if(grepl("926614|926620", x)) '#E78AC3' #1-TOR-2
  else if(grepl("839425|839428|839431|839434", x)) '#A6D854' #0-BatSRBD
}))

#ages=c("52 weeks","20-23 weeks","<10 week")
#agecolbrew = brewer.pal(3, "Set3")
agecolors <- unlist(lapply(rownames(hmdata1),function(x){
  if(grepl("867451|867460|867469|867457|867466|867475|867454|867463|867472", x)) '#8DD3C7' #old 52wk
  else if(grepl("494014|494017|494020|494023|821644|823390|839437|494026|494029|494032|494035|821650|823396|839440|494038|494041|494044|494047|821656|823402|839443|833452|840316|834109|494050|494053|494056|494011|821662|823408|839446|840319|834112|839425|839428|839431|839434", x)) '#FFFFB3' #mid 20-23wk
  else if(grepl("867478|867487|867496|833449|1326109|957616|995281|867505|685244|685187|685193|957619|995284|685247|685178|685217|833455|995287|867484|867493|867502|867511|867481|867490|867499|867508|926614|926620", x)) '#BEBADA' #young <10wk
}))

annotCols=cbind(dpicolors,straincolors,agecolors)
colnames(annotCols)[1]="DPI"
colnames(annotCols)[2]="SARS Strain"
colnames(annotCols)[3]="Age"

hmdatat=t(hmdata1)

yeblbupal = colorRampPalette(c("blue","blue2","blue3","blue4","black","yellow4","yellow3","yellow2","yellow"))

# #For custom ordering, add rowv arg to heatmap.plus function to apply
# rowDistance = dist(hmdatat, method = "euclidean")
# rowCluster = hclust(rowDistance, method = "single")
# rowDend = as.dendrogram(rowCluster)
# rowDend = reorder(rowDend, rowMeans(hmdatat))

heatmap.plus(hmdatat, col=yeblbupal(27), scale=c("none"), ColSideColors = annotCols)
#heatmap.plus(hmdatat, col=bluered(27), scale=c("none"), ColSideColors = annotCols, Rowv=rowDend)
#legend("topleft", legend=paste(dpitimes,"dpi"), fill=dpicolbrew,cex=0.75)
#legend(0.5,1.3, legend=paste(strains), fill=straincolbrew,cex=0.75)
#legend(0.7,1.4, legend=paste(ages), fill=agecolbrew,cex=0.75)
