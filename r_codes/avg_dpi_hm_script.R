#Mike Edwards 74 biosets heatmap average dpi across 760 genes selected to contain bex2, cxcl10 and all genes from cxcl2 to top of list sorted for most time points (760 genes total)
#Chase McFarland
library(heatmap.plus)
library(gplots)
library(gtools)
library(RColorBrewer)
library(dplyr)

#Read raw data file, setwd() to file location
rawDat = read.csv("3bv2_ave_dpi_genes.csv",TRUE,",")
row.names(rawDat)=rawDat[,1] #set row names as genes in col 1
parsedDat = select(rawDat,-1) #delete col 1
rawDatnocol1 = select(rawDat,-1)

yeblbupal = colorRampPalette(c("blue","blue2","blue3","blue4","black","yellow4","yellow3","yellow2","yellow"))

bex2Cols <- unlist(lapply(rownames(rawDatnocol1),function(x){
  if(grepl("7920|8372|7307|9368|667|4558|2158|6522|5433|5140|8368|8210|8827|8234|5950|6626|8204|5537|1595|2317|2668|7245|8770|8209|1005|1640|1186|1306|2256|8150|6199|9684|1441|5841|3567|6103|9555|5363|8643|1774|8152|8156|2080|2732|7090|8154|2031|6629|942|2281|1226",x)) '#0400FF' #Bex2 Cluster
  else '#000000'
}))



cxcl10Cols <- unlist(lapply(rownames(rawDatnocol1),function(x){
  if(grepl("1226|6618|6102|4952|6101|6098|9365|1233|6615|2322|3767|754|8328|8327|1988|1994|6113|2730|2728|1986|6619|8089|4845|6174|1990|2729|6610|5048|10264|5036|9005|614|6985|4597|2724|2448|1577|4846|4911|5039|4934|6175|4847|10010|4848|4841|4834|8677|4840|6617|4839",x)) '#F0FF00' #Cxcl10 Cluster
  else '#000000'
}))


rowAnnot=cbind(bex2Cols,cxcl10Cols)
colnames(rowAnnot)[1]="Bex2 Cluster"
colnames(rowAnnot)[2]="Cxcl10 Cluster"

#hm = heatmap.plus(as.matrix(parsedDat), col=yeblbupal(27), scale=c("none"), keep.dendro=TRUE)
heatmap.plus(as.matrix(rawDatnocol1), col=yeblbupal(27), scale=c("none"),RowSideColors = rowAnnot, keep.dendro=TRUE) #Col indicies go from bottom to top

hmgenedendro=as.hclust(hm$Rowv) #NOT ACTUALLY IN ORDER WTF
hmgeneorder=as.list(hmgenedendro$order)
hmgenenames=as.list(hmgenedendro$labels)

