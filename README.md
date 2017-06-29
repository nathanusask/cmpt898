# cmpt898
<<<<<<< HEAD
# To use the python code for SNP data preprocessing, PyVCF needs to be installed beforehand
=======
>>>>>>> 5b36d1ac4d405e965b1fc5035c001b6937518702

source-code/vcf_melt 
	this is basically a python script copied and slightly modified from the PyVCF package
	this script separates each SNP record into samples and store all the information into a csv file
	this script is generally a test case at this point

source-code/SNP_filter.py
	This script does the following steps:
		1. filter out records that are indels, meanwhile, count appearance for each sample whose 'GT' field is not empty
		2. calculate for each SNP record's MAF and filter out the record whose MAF , 0.01
		3. SNP records with MAF < 0.01 or are indels will be removed
		4. samples with misssing rate > 10% will be removed

	Package PyVCF should be installed prior to running this program
	Make sure your python interpreter includes that package

source-code/SNP_preprocessing.py
	This script is basically a demo of using the PyVCF package

Limited by the capacity of git project and other concerns, data files are not shared here.
