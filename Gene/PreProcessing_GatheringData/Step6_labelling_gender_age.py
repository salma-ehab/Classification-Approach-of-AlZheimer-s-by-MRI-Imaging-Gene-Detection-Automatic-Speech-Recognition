import pandas as pd
from tqdm import tqdm
import os
import shutil
import math


def labelling(gene_csv_file,diagnosis_csv_file):
       diagnosis_array=[]

       df_gene_patients = pd.read_csv(gene_csv_file, usecols = ['ID']) 
       df_gene_patients_array = df_gene_patients.values 

       df_diagnosis = pd.read_csv(diagnosis_csv_file, usecols = ['PTID','DXCURREN'])
       df_diagnosis_array = df_diagnosis.values 
       diag_dict = {1.0: 1, 2.0: 2,3.0:3}
       df_diagnosis['DXCURREN'] = df_diagnosis['DXCURREN'].map(diag_dict) 
       df_diagnosis_array = df_diagnosis.values   

       for item in  df_gene_patients_array:
        for other_item in  df_diagnosis_array:
                if item[0] == other_item[0]:
                        diagnosis_array.append(other_item[1])
                        break
        
       print(diagnosis_array)
       print("------------------------------------------------------------------------------")
       csv_file= pd.read_csv(gene_csv_file)    
       csv_file['label'] = diagnosis_array
       csv_file.to_csv(gene_csv_file)

       

def get_gender_age(gene_csv_file,demographics_csv_file,diagnosis_csv_file):
        gender_array = []
        age_array = []
        RID_array = []

        df_gene_patients = pd.read_csv(gene_csv_file, usecols = ['ID']) 
        df_gene_patients_array = df_gene_patients.values 

        df_demographics = pd.read_csv(demographics_csv_file, usecols = ['RID','PTGENDER','USERDATE','PTDOBMM','PTDOBYY']) 
        #gender_dict = {1.0: "M", 2.0: "F"}
        #gender_dict = {1.0: 1, 2.0: 2}
        #df_demographics['PTGENDER'] = df_demographics['PTGENDER'].map(gender_dict) 
        df_demographics_array = df_demographics.values 

        df_diagnosis = pd.read_csv(diagnosis_csv_file, usecols = ['RID','PTID']) 
        df_diagnosis_array = df_diagnosis.values       

        for index in range(len(df_gene_patients_array)):
                for index2 in range(len(df_diagnosis_array)):
                        if (df_diagnosis_array[index2][1] == df_gene_patients_array[index][0]):
                                RID_array.append(df_diagnosis_array[index2][0])
                                break

        for index in range(len(df_gene_patients_array)):
                for index2 in range(len(df_demographics_array)):
                        if (RID_array[index]== df_demographics_array[index2][0]):
                                gender_array.append(df_demographics_array[index2][2])

                                splitted_user_date = df_demographics_array[index2][1].split("-")
                                user_date_year = splitted_user_date[0]
                                user_date_month = splitted_user_date[1]

                                if (math.isnan(df_demographics_array[index2][4])==False):
                                        if (int(user_date_month) >= int(df_demographics_array[index2][3])):
                                                age_array.append(int(user_date_year)- int(df_demographics_array[index2][4]))
                                        
                                        else:
                                                age_array.append(int(user_date_year)- int(df_demographics_array[index2][4])-1)

                                break

       
        print(gender_array)
        print("------------------------------------------------------------------------------")
        csv_file= pd.read_csv(gene_csv_file)    
        csv_file['gender'] = gender_array
        csv_file.to_csv(gene_csv_file)

        print(age_array)
        print("------------------------------------------------------------------------------")
        csv_file= pd.read_csv(gene_csv_file)    
        csv_file['age'] = age_array
        csv_file.to_csv(gene_csv_file)
       
                
         


gene_csv_file = "F:\Graduation Project\Gene\Final_Adni1\Gene_Data_3.csv"
diagnosis_csv_file="F:\Graduation Project\Gene\Final_Gene_Data\DXSUM_PDXCONV_ADNIALL.csv"
demographics_csv_file="F:\Graduation Project\Gene\Final_Gene_Data\PTDEMOG.csv"
labelling(gene_csv_file,diagnosis_csv_file)
get_gender_age(gene_csv_file,demographics_csv_file,diagnosis_csv_file)













    

     






