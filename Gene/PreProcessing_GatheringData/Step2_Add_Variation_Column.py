import pandas as pd
from tqdm import tqdm
import os


def add_variation(file_path):

    allele_1=[]
    allele_2=[]
    ref_allele=[]
    variation=[]

    df_allele_1= pd.read_csv(file_path, usecols = ['Allele1 - Forward'])
    df_array_allele_1 = df_allele_1.values
    for item in df_array_allele_1 :
        for inner_item in item:
            allele_1.append(inner_item)


    df_allele_2= pd.read_csv(file_path, usecols = ['Allele2 - Forward'])
    df_array_allele_2 = df_allele_2.values
    for item in df_array_allele_2 :
        for inner_item in item:
            allele_2.append(inner_item)

    df_ref_allele= pd.read_csv(file_path, usecols = ['ref_allele'])
    df_array_ref_allele = df_ref_allele.values
    for item in df_array_ref_allele :
        for inner_item in item:
            ref_allele.append(inner_item)

       
    for i in range(len(ref_allele)):
        if((ref_allele[i] == allele_1[i]) and (ref_allele[i] == allele_2[i])):
            variation.append(0)
            
        elif ((ref_allele[i] != allele_1[i]) and (ref_allele[i] == allele_2[i]) or ((ref_allele[i] == allele_1[i]) and (ref_allele[i] != allele_2[i]))):
            variation.append(1)

        elif ((ref_allele[i] != allele_1[i]) and (ref_allele[i] != allele_2[i])):
            variation.append(2)

    csv_file= pd.read_csv(file_path)    
    csv_file['allele_variation'] = variation
    csv_file.to_csv(file_path)



data_Path = "F:\Graduation Project\Gene\Adni1_Sets\Set 3"


for m in tqdm(os.listdir(data_Path)):
    add_variation(os.path.join(data_Path,m))






    


