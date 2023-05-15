import pandas as pd
from tqdm import tqdm
import os
import shutil


def check_snps(csvPath,csv_file_1_path):
    df_snp_csv_1 = pd.read_csv(csv_file_1_path, usecols = ['SNP Name']) 
    df_snp_csv_1_array = df_snp_csv_1.values 

    for m in tqdm(os.listdir(csvPath)):
       
        df_snp = pd.read_csv(os.path.join(csvPath,m), usecols = ['SNP Name']) 
        df_snp_array = df_snp.values 
        
       

        for index in range(len(df_snp_array)):
            if index <= len(df_snp_csv_1_array)-1:
                if df_snp_csv_1_array[index] != df_snp_array[index]:
                    print("Different Snp is:",df_snp_array[index])
                    print("Patient ID is:",m)
                    print("-----------------------------------")
                    




     
     
     
     

   
data_path = "F:\Graduation Project\Gene\Adni1_Sets\Set 3"
csv_file_1_path = "F:\Graduation Project\Gene\Adni1_Sets\Check_snps\S_002_S_0295.csv"
check_snps(data_path,csv_file_1_path)










