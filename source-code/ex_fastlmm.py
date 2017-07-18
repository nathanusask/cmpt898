#!/Users/xuy962/anaconda/envs/py27/bin/python

# import argparse
from pysnptools.snpreader import Bed
from fastlmm.association import single_snp

# Parser allows the script to take a phenotype file and output file as arguments
# parser = argparse.ArgumentParser()
# parser.add_argument('pheno_file')
# parser.add_argument('out_file')
# args = parser.parse_args()

# Providing the path to the bed file required for analysis
bed_file = '../source-data/pheno-data/KP_aggregate.bed'
pheno_file = '../source-data/pheno-data/pheno_aggregate1.sorted.phe'
cov_fn = '../source-data/pheno-data/KP_aggregate.cov'
out_file = '../source-data/fastlmm_all_w_cov'

# Perform the single_snp GWAS analysis.
# By default, FaST-LMM does not generate a proper output file so the output_file_name option
# is required. An arbitrary RAM cap of 10G was set based on previous tests.
# results_df = single_snp(bed_file, args.pheno_file, GB_goal=10, count_A1=True, output_file_name=args.out_file)
results_df = single_snp(bed_file, pheno_file, covar=cov_fn, GB_goal=10, count_A1=True, output_file_name=out_file)

# Tools for visualization if you're equipped with Xquartz (my Desktop machine is not...)
import pylab
import fastlmm.util.util as flutil
# import matplotlib.pyplot as plt
flutil.manhattan_plot(results_df.as_matrix(["Chr", "ChrPos", "PValue"]),pvalue_line=1e-5,xaxis_unit_bp=False)
pylab.show()

from fastlmm.util.stats import plotp
plotp.qqplot(results_df["PValue"].values, xlim=[0,5], ylim=[0,5])
# plt.show()

import panda as pd
pd.set_option('display.width', 1000)
results_df.head(n=20)
