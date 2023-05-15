import pandas as pd
from tqdm import tqdm
import os
import shutil

   
def filter_VCF_File(vcfFile):
    df = pd.read_csv(vcfFile,sep="\t",comment='#')
    filter_chr = df[(df['CHROM'] != 'chr1') & (df['CHROM'] != 'chr14') & (df['CHROM'] != 'chr19') & (df['CHROM'] != 'chr21')].index
    df.drop(filter_chr, inplace=True)
    df.to_csv(vcfFile, index=False)


def get_snp_refAllele(vcfFile):
    snp_vcf = []
    refAllele_vcf = []
    snp_vcf_2 = []
    refAllele_vcf_2= []

    df_vcf = pd.read_csv(vcfFile,sep="\t")
    VCF_Array = df_vcf.values 
    for item in VCF_Array:
        for inner_item in item:
            splitted_array = inner_item.split(',')
            snp_vcf.append(splitted_array[2])
            refAllele_vcf.append(splitted_array[3])
    
    for index in range(len(snp_vcf)):
        if (snp_vcf[index] != '.'):
             if (";" in snp_vcf[index]):
                  split_snps = snp_vcf[index].split(";")
                  for index2 in range(len(split_snps)):
                      snp_vcf_2.append(split_snps[index2])
                      refAllele_vcf_2.append(refAllele_vcf[index])
                
             else:
                 snp_vcf_2.append(snp_vcf[index])
                 refAllele_vcf_2.append(refAllele_vcf[index])
        
    return snp_vcf_2, refAllele_vcf_2


def get_snp_csv(csvPath):
    snp_csv = []
    df_csv = pd.read_csv(csvPath,usecols=['SNP Name'])
    SNP_Array = df_csv.values 
    for item in SNP_Array:
        for inner_item in item:
            snp_csv.append(inner_item)

    return snp_csv




def getRefAllele_vcf_1(csvPath,vcfFile1,final_ref_allele):

    #get snp name and corresponding ref allele from vcf
    snp_vcf_1, refAllele_vcf_1 = get_snp_refAllele(vcfFile1)

    #get snp name from csv file
    snp_csv=get_snp_csv(csvPath)

    #compare snp in vcf file with snp in csv file 1
    found = False
    for item_csv in snp_csv:
        for i in range(len(snp_vcf_1)):
            if (item_csv == snp_vcf_1[i]):
                found = True
                final_ref_allele.append(refAllele_vcf_1[i])
                break

        if found:
            found = False
        else:
            final_ref_allele.append("-")

    return final_ref_allele



def getRefAllele_other_vcf(csvPath,other_vcf,final_ref_allele):

    #get snp name and corresponding ref allele from vcf
    snp_other_vcf, refAllele_other_vcf = get_snp_refAllele(other_vcf)
    
    #get snp name from csv file
    snp_csv=get_snp_csv(csvPath)


    #compare snp in vcf file with snp in other vcf
    for j in range(len(snp_csv)):
        if(final_ref_allele[j]=="-"):
              for i in range(len(snp_other_vcf)):
                if (snp_csv[j] == snp_other_vcf[i]):
                    final_ref_allele[j]=refAllele_other_vcf [i]
                    break

    return final_ref_allele


csvPath="F:\Graduation Project\Gene\Adni1_Sets\Check_snps\S_002_S_0295.csv"
vcfFile_1 ="F:\Graduation Project\Gene\snp\ADNI_002_S_0413_SNPs.vcf"
vcf_Other_Path="F:\Graduation Project\Gene\snpUsed"
vcf_Other_Path_2="F:\Graduation Project\Gene\snpUsed2"


final_ref_allele=[]
final_ref_allele = getRefAllele_vcf_1(csvPath,vcfFile_1 ,final_ref_allele)
print(final_ref_allele)
print("------------------------------------------------------------------")

for m in tqdm(os.listdir(vcf_Other_Path)):
    #filter_VCF_File(os.path.join(vcf_Other_Path,m))
    final_ref_allele = getRefAllele_other_vcf(csvPath,os.path.join(vcf_Other_Path,m),final_ref_allele)
    print(final_ref_allele)
    print("------------------------------------------------------------------")

for m in tqdm(os.listdir(vcf_Other_Path_2)):
    #filter_VCF_File(os.path.join(vcf_Other_Path_2,m))
    final_ref_allele = getRefAllele_other_vcf(csvPath,os.path.join(vcf_Other_Path_2,m),final_ref_allele)
    print(final_ref_allele)
    print("------------------------------------------------------------------")

#add ref_allele to csv file
csv_file= pd.read_csv(csvPath)    
csv_file['ref_allele'] = final_ref_allele
csv_file.to_csv(csvPath)




