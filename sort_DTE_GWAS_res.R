#!/usr/local/bin/R

setwd("~/Downloads/plink_mac/")
lr_dte_gwas_res <- read.table("KP_GWAS_G_E_DTE.assoc.linear", header=T)

lr_dte_gwas_res_add <- lr_dte_gwas_res[lr_dte_gwas_res$TEST=="ADD",]
lr_dte_gwas_res_add_sorted <- lr_dte_gwas_res_add[order(lr_dte_gwas_res_add$P),]

lr_dte_gwas_res_pcp <- lr_dte_gwas_res[lr_dte_gwas_res$TEST=="Precipitation",]
lr_dte_gwas_res_pcp_sorted <- lr_dte_gwas_res_pcp[order(lr_dte_gwas_res_pcp$P),]

lr_dte_gwas_res_sw <- lr_dte_gwas_res[lr_dte_gwas_res$TEST=="Seedwt",]
lr_dte_gwas_res_sw_sorted <- lr_dte_gwas_res_sw[order(lr_dte_gwas_res_sw$P),]

lr_dte_gwas_res_dl <- lr_dte_gwas_res[lr_dte_gwas_res$TEST=="DayLength",]
lr_dte_gwas_res_dl_sorted <- lr_dte_gwas_res_dl[order(lr_dte_gwas_res_dl$P),]

lr_dte_gwas_res_yr <- lr_dte_gwas_res[lr_dte_gwas_res$TEST=="Year",]
lr_dte_gwas_res_yr_sorted <- lr_dte_gwas_res_yr[order(lr_dte_gwas_res_yr$P),]

lr_dte_gwas_res_loc <- lr_dte_gwas_res[lr_dte_gwas_res$TEST=="Location",]
lr_dte_gwas_res_loc_sorted <- lr_dte_gwas_res_loc[order(lr_dte_gwas_res_loc$P),]

head(lr_dte_gwas_res_add_sorted)
head(lr_dte_gwas_res_pcp_sorted)
head(lr_dte_gwas_res_sw_sorted)
head(lr_dte_gwas_res_dl_sorted)
head(lr_dte_gwas_res_yr_sorted)
head(lr_dte_gwas_res_loc_sorted)

write.table(lr_dte_gwas_res_loc_sorted, "~/Documents/cmpt898/lr_dte_gwas_res_loc_sorted", sep="\t", quote=FALSE, append=FALSE)
write.table(lr_dte_gwas_res_yr_sorted, "~/Documents/cmpt898/lr_dte_gwas_res_yr_sorted", sep="\t", quote=FALSE, append=FALSE)
write.table(lr_dte_gwas_res_dl_sorted, "~/Documents/cmpt898/lr_dte_gwas_res_dl_sorted", sep="\t", quote=FALSE, append=FALSE)
write.table(lr_dte_gwas_res_sw_sorted, "~/Documents/cmpt898/lr_dte_gwas_res_sw_sorted", sep="\t", quote=FALSE, append=FALSE)
write.table(lr_dte_gwas_res_pcp_sorted, "~/Documents/cmpt898/lr_dte_gwas_res_pcp_sorted", sep="\t", quote=FALSE, append=FALSE)
write.table(lr_dte_gwas_res_add_sorted, "~/Documents/cmpt898/lr_dte_gwas_res_add_sorted", sep="\t", quote=FALSE, append=FALSE)