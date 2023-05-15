import pandas as pd
from tqdm import tqdm
import os


def drop_column(file_path):
     csv_file= pd.read_csv(file_path,index_col=0)   
     csv_file.drop(['Unnamed: 0', 'Sample Index','GC Score','SNP Index','Allele1 - Top','Allele2 - Top','Allele1 - Forward',
     'Allele2 - Forward','Allele1 - AB','Allele2 - AB','Chr','Position','GT Score','Cluster Sep','SNP','Theta','R','X','Y','X Raw'
    ,'Y Raw','B Allele Freq','Log R Ratio','ref_allele'], axis=1,inplace=True)
     csv_file.to_csv(file_path)

def drop_column_id(file_path):
     csv_file= pd.read_csv(file_path,index_col=0)   
     csv_file.drop(['Sample ID'], axis=1,inplace=True)
     csv_file.to_csv(file_path)

            
data_Path = "F:\Graduation Project\Gene\Adni1_Sets\Set 3"

for m in tqdm(os.listdir(data_Path)):
    drop_column(os.path.join(data_Path,m))


for m in tqdm(os.listdir(data_Path)):
    drop_column_id(os.path.join(data_Path,m))






    


