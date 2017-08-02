#
#
#              Diabetes Genetics Initiative of Broad Institute of Harvard and MIT, Lund University and
#                                  Novartis Institutes of BioMedical Research
#        Whole-genome association analysis identifies novel loci for type 2 diabetes and triglyceride levels
#                             Science 2007 Jun 1;316(5829):1331-6. Epub 2007 Apr 26
#
#
#
setwd("~/Documents/cmpt898/source-data")
pvals <- read.table("fastlmm_all_w_cov", header=T)

observed <- sort(pvals$PValue)
lobs <- -(log10(observed))

expected <- c(1:length(observed)) 
lexp <- -(log10(expected / (length(expected)+1)))



pdf("qqplot_fastlmm.pdf", width=5, height=5)
plot(c(0,5), c(0,5), col="red", lwd=3, type="l", xlab="Expected (-logP)", ylab="Observed (-logP)", xlim=c(0,5), ylim=c(0,5), las=1, xaxs="i", yaxs="i", bty="l")
points(lexp, lobs, pch=15, cex=.4, bg="black") 
dev.off()


