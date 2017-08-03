#!/Users/xuy962/anaconda/envs/py27/bin/python

import argparse
from pysnptools.snpreader import Bed
from fastlmm.association import single_snp

# Parser allows the script to take a phenotype file and output file as arguments
parser = argparse.ArgumentParser()
parser.add_argument('bed_file')
parser.add_argument('pheno_file')
parser.add_argument('out_file')
parser.add_argument('plot_title')
args = parser.parse_args()

# Providing the path to the bed file required for analysis
# bed_file = "/birl2/users/cbe453/arabidopsis-association/PLINK_manipulation/Seed_Oil_Composition_maf_ge_05_Fully_Merged_391_Subset_Final"
#pheno_file = "/birl2/data/P2IRC/GE2P/GWAS/arabidopsis/arabidopsis-pheno-files/BC16_0/bioBC_FA-BC16_0_plink.pheno"

# Perform the single_snp GWAS analysis.
# By default, FaST-LMM does not generate a proper output file so the output_file_name option
# is required. An arbitrary RAM cap of 10G was set based on previous tests.
results_df = single_snp(args.bed_file, args.pheno_file, GB_goal=10, count_A1=True, output_file_name=args.out_file)

# Tools for visualization if you're equipped with Xquartz (my Desktop machine is not...)
import matplotlib.pyplot as plt
import fastlmm.util.util as flutil
#draw manhattan plot
flutil.manhattan_plot(results_df.as_matrix(["Chr", "ChrPos", "PValue"]),pvalue_line=1e-5,xaxis_unit_bp=False)
plt.title(args.plot_title)
plt.savefig(args.out_file + '.png')

#draw qqplot
from fastlmm.util.stats.plotp import qqplot
qqplot(results_df["PValue"].values, fileout='qq_' + args.out_file + '.png', title=args.plot_title.replace('Manhattan', 'Quantile-quantile'))

results_df.head()
