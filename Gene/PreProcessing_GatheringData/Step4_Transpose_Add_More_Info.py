import pandas as pd
from tqdm import tqdm
import os


def transpose(file_path):

     csv_file= pd.read_csv(file_path,index_col = 0)   
     csv_file= csv_file.set_index('SNP Name').T.reset_index()
     csv_file.to_csv(file_path,index=False)

def add_id(folder_path):

    for m in tqdm(os.listdir(folder_path)):
         items = m.split('.')
         id = items[0]
         csv_file= pd.read_csv(os.path.join(folder_path,m),index_col=0)
         csv_file.insert(0, 'ID', id)
         csv_file.to_csv(os.path.join(folder_path,m),index = False)

def add_more_info(folder_path,MRI_CSV_path):

    df = pd.read_csv(MRI_CSV_path, usecols = ['Subject', 'Group','Sex','Age'])        
    df_dtypes = df.infer_objects()                         
    CSVArray = df.values 
    for m in tqdm(os.listdir(folder_path)):
        items = m.split('.')
        id = items[0]
        for item in CSVArray:
            if (item[0]  == id):
                 csv_file= pd.read_csv(os.path.join(folder_path,m))
                 csv_file.insert(1, 'Group', item[1])
                 csv_file.insert(2, 'Sex', item[2])
                 csv_file.insert(3, 'Age', item[3])
                 csv_file.to_csv(os.path.join(folder_path,m))
                 break




            
data_path = "F:\Graduation Project\Gene\Adni1_Sets\Set 3"
#MRI_csv="F:\Graduation Project\Gene\CSV_File\ADNI1_Screening_1.5T_12_08_2022.csv"


for m in tqdm(os.listdir(data_path)):
    transpose(os.path.join(data_path,m))


add_id(data_path)


#add_more_info(CN_Path,MRI_csv)
#add_more_info(AD_Path,MRI_csv)
#add_more_info(MCI_Path,MRI_csv)







    


