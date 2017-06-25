#author: Nathan Yang
#Date created: Jun 24, 2017
'''
This python program requires PyVCF to be installed

Pre-processing of VCF file to extract SNP data with only ID, POS, REF and ALT stored
'''

import vcf
import csv

with open('.vcf', 'r') as vcffile:
	vcf_reader = vcf.Reader(vcffile)
	with open('SNP_filter.csv', 'w') as csvfile:
		fieldnames = ['ID', 'POS', 'REF', 'ALT']
		csvWriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
		csvWriter.writeheader()
		for record in vcf_reader:
			if record.is_indel:
				continue
			if not record.is_snp:
				continue
			csvWriter.writerow({'ID': record.ID,
					'POS': record.POS,
					'REF': record.REF,
					'ALT': record.ALT
					})
	csvfile.close()
vcffile.close()

