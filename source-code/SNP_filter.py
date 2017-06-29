'''
There are two steps:
1. filter out records that are indels, meanwhile, count appearance for each sample whose 'GT' field is not empty
2. calculate for each SNP record's MAF and filter out the record whose MAF , 0.01
3. SNP records with MAF < 0.01 or are indels will be removed
4. samples with misssing rate > 10% will be removed

Package PyVCF should be installed prior to running this program
Make sure your python interpreter includes that package
'''

import vcf
import csv

def calc_maf(record):
    '''
    calculate the minor allele frequency for each record
    :param record: one record in vcf_reader
    :return: maf
    -1 means the record is basically useless;
    0 means there is no minor allele to investigate
    otherwise, whether or not the record is useful depends on the MAF threshold (by default it's 0.01)
    '''
    if record.is_indel or not record.is_snp:
        #meaning this SNP record is not useful
        return -1
    if record.call_rate == record.num_hom_ref:
        #meaning that all the genotypes are homozygous
        return 0

    ref, alt1, alt2 = 0, 0, 0
    for sample in record.samples:
        if sample['GT'] == '.':
            continue
        if sample.phased:
            if sample['GT'] == '.|.':
                continue
            if not sample.is_het:
                #homozygous, needs to determine hom_ref or hom_alt
                idx = int(sample['GT'].split('|')[0])
                if idx == 0:
                    #hom_ref
                    ref += 2*sample['AD'][0]
                elif idx == 1:
                    #hom_alt1
                    alt1 += 2*sample['AD'][1]
                else:
                    alt2 += 2*sample['AD'][1]
            else:
                #hom_het
                idx1, idx2 = int(sample['GT'].split('|'))
                if idx1 == 0:
                    ref += sample['AD'][0]
                elif idx1 == 1:
                    alt1 += sample['AD'][1]
                elif idx1 == 2:
                    alt2 += sample['AD'][1]
                elif idx2 == 0:
                    ref += sample['AD'][0]
                elif idx2 == 1:
                    alt1 += sample['AD'][1]
                elif idx2 == 2:
                    alt2 += sample['AD'][1]
                else:
                    continue
        else:
            if sample['GT'] == './.':
                continue
            if not sample.is_het:
                #homozygous, needs to determine hom_ref or hom_alt
                idx = int(sample['GT'].split('/')[0])
                if idx == 0:
                    #hom_ref
                    ref += 2*sample['AD'][0]
                elif idx == 1:
                    #hom_alt1
                    alt1 += 2*sample['AD'][1]
                else:
                    alt2 += 2*sample['AD'][1]
            else:
                #hom_het
                idx1, idx2 = [int(x) for x in sample['GT'].split('/')]
                if idx1 == 0:
                    ref += sample['AD'][0]
                elif idx1 == 1:
                    alt1 += sample['AD'][1]
                elif idx1 == 2:
                    alt2 += sample['AD'][1]
                elif idx2 == 0:
                    ref += sample['AD'][0]
                elif idx2 == 1:
                    alt1 += sample['AD'][1]
                elif idx2 == 2:
                    alt2 += sample['AD'][1]
                else:
                    continue

    total = ref + alt1 + alt2
    af1 = float(alt1)/total
    af2 = float(alt2)/total

    return max(af1, af2)

def main():
    vcffile = open('../source-data/may24_17_af2_m20_ordered.vcf')
    #make sure you have your vcf file prepared or you may modify the path of ypur file here
    vcf_reader = vcf.Reader(vcffile)
    dict_samples = {}
    samples = vcf_reader.samples
    for sample in samples:
        sample_name = sample
        dict_samples[sample_name] = {}
        dict_samples[sample_name]['count'] = 0
        # dict_samples[sample_name]['CHROM'] = {}

    valid_snps_count = 0

    for record in vcf_reader:
        if calc_maf(record) > 0.01:
            valid_snps_count += 1
            lst_alleles = [record.REF]
            lst_alleles += [record.ALT]
            chrom = 'chr_' + str(record.CHROM)
            cpos = record.POS
            cref = record.REF
            calt = record.ALT
            cid = record.ID
            for sample in record.samples:
                if not sample.called:
                    continue
                sample_name = sample.sample
                dict_samples[sample_name]['count'] += 1
                dict_samples[sample_name][chrom] = {}
                dict_samples[sample_name][chrom]['name'] = chrom
                dict_samples[sample_name][chrom]['ID'] = cid
                dict_samples[sample_name][chrom]['POS'] = cpos
                dict_samples[sample_name][chrom]['REF'] = cref
                dict_samples[sample_name][chrom]['ALT'] = calt
                dict_samples[sample_name][chrom]['GT'] = sample['GT']
                dict_samples[sample_name][chrom]['AD'] = sample['AD']


    vcffile.close()

    csvfile = open('../source-data/filtered_SNP.csv', 'w')
    fieldnames = ['sample', 'chrom', 'chrom_id', 'chrom_pos', 'REF', 'ALT', 'GT', 'AD']
    csvWriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
    csvWriter.writeheader()
    for sample in samples:
        rate = dict_samples[sample]['count'] / valid_snps_count
        if rate >= 0.90:
            for chrom in dict_samples[sample].keys():
                if chrom == 'count':
                    continue
                csvWriter.writerow({'sample': sample,
                                    'chrom': dict_samples[sample][chrom]['name'],
                                    'chrom_id': dict_samples[sample][chrom]['ID'],
                                    'chrom_pos': dict_samples[sample][chrom]['POS'],
                                    'REF': dict_samples[sample][chrom]['REF'],
                                    'ALT': dict_samples[sample][chrom]['ALT'],
                                    'GT': dict_samples[sample][chrom]['GT'],
                                    'AD': dict_samples[sample][chrom]['AD']
                                    })
        else:
            continue

    dict_samples.clear()
    print('Filtering of SNP data: done!')
    csvfile.close()

if __name__ == '__main__':
    main()
