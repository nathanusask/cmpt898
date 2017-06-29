#author: Nathan Yang
#Date created: Jun 24, 2017
'''
This python program requires PyVCF to be installed

Pre-processing of VCF file to extract SNP data with only ID, POS, REF and ALT stored
'''

import vcf
import csv


def parseGT(strGT):
    index = 0
    if strGT.find('\\') > 0:
        index = strGT.index('\\')
    elif strGT.find('|') > 0:
        index = strGT.index('|')
    else:
        return []
    return [int(strGT[:index]), int(strGT[index+1:])]

def get_variant_type(record):
    lst_ret = []
    for sample in record:
        if not sample.called:
            lst_ret.append('no_call')
        elif hasattr(sample.data, 'GQ') and sample.data.GQ == 0:
            lst_ret.append('no_call')
        elif not sample.is_variant:
            lst_ret.append('hom_ref')
        elif sample.is_het:
            lst_ret.append('het')
        else:
            lst_ret.append('hom_alt')
    return lst_ret

def main():
    dict_snps = {}
    lst_samples = []  # keep only those sample names

    with open('../source-data/may24_17_af2_m20_ordered.vcf', 'r') as vcffile:
        # add the VCF filename here
        vcf_reader = vcf.Reader(vcffile)
        # vcf_reader.samples
        for sample in vcf_reader.samples:
            lst_samples.append(sample.sample)

        # with open('../source-data/SNP_filter.csv', 'w') as csvfile:
        #     fieldnames = ['ID', 'POS', 'REF', 'ALT']
        #     # there's no visualization done in this program
        #     csvWriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        # csvWriter.writeheader()
        for record in vcf_reader:
            if record.is_indel:
                continue
            if not record.is_snp:
                continue
            tmp_record_id = record.ID
            lst_ref = record.REF
            lst_alt = record.ALT
            dict_snps[tmp_record_id] = {}
            dict_snps[tmp_record_id]['alleles'] = lst_ref + lst_alt
        for sample in lst_samples:
            # TODO: complete adding alleles here
            # TODO: need to extract the genotype into separate alleles
            tmp_l = parseGT(sample['GT'])
            first_allele = dict_snps[tmp_record_id]['allele'][tmp_l[0]]
            second_allele = dict_snps[tmp_record_id]['allele'][tmp_l[1]]
            dict_snps[tmp_record_id][sample] = []
        #     csvWriter.writerow({'ID': tmp_record_id,
        #                         'POS': record.POS,
        #                         'REF': lst_ref,
        #                         'ALT': lst_alt
        #                         })
        # csvfile.close()
    vcffile.close()

if __name__ == '__main__':
    main()

