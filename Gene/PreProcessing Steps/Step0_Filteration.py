import pandas as pd
from tqdm import tqdm
import os
import shutil


def filtering(csvPath):
    for m in tqdm(os.listdir(csvPath)):
        df = pd.read_csv(os.path.join(csvPath,m))
        snp_name = df['SNP Name'].astype(str)
        filtered_chr_snp_geneLocation = df[(df['Chr'] != '1') & (df['Chr'] != '14') & (df['Chr'] != '19') & (df['Chr'] != '21') | (~snp_name.str.startswith('rs')) 
        | ((df['Chr'] == '19') & ((df['Position']<50090879) | (df['Position']>50114490))) | ((df['Chr'] == '14') & ((df['Position']<72662932) | (df['Position']>72766862)))
        | ((df['Chr'] == '1') & ((df['Position']<225114896) | (df['Position']>225160427))) | ((df['Chr'] == '21') & ((df['Position']<26164732) | (df['Position']>26475003)))].index
        df.drop(filtered_chr_snp_geneLocation, inplace=True)
        df.to_csv(os.path.join(csvPath,m), index=False)

   
data_path = "F:\Graduation Project\Gene\Adni1_Sets\Set 3"
filtering(data_path)










