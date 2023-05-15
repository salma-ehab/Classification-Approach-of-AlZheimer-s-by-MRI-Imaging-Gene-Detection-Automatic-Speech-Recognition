import pandas as pd
from tqdm import tqdm
import os


def read_column_drop(csv_file):
    ref_allele = []
    df = pd.read_csv(csv_file, usecols = ['ref_allele'])                             
    ref_Array = df.values 
     
    for item in  ref_Array:
        for inner_item in item:
            ref_allele .append(inner_item)

    return ref_allele 


def add_ref_allele_column(Folder_path,ref_allele_array):
    for m in tqdm(os.listdir(Folder_path)):
        csv_file= pd.read_csv(os.path.join(Folder_path,m))    
        csv_file['ref_allele'] = ref_allele_array
        csv_file.to_csv(os.path.join(Folder_path,m))



csv_file_path = "F:\Graduation Project\Gene\Adni1_Sets\Check_snps\S_002_S_0295.csv"
data_Path = "F:\Graduation Project\Gene\Adni1_Sets\Set 3"


refAllele = read_column_drop(csv_file_path)
print(refAllele)
add_ref_allele_column(data_Path,refAllele)





    


