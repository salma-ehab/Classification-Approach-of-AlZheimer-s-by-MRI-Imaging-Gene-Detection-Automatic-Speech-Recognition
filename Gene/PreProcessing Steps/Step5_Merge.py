import pandas as pd
from tqdm import tqdm
import os

def merge(data_path,merged_data_path):
    df_csv_append = pd.DataFrame()
    for m in tqdm(os.listdir(data_path)):
        df = pd.read_csv(os.path.join(data_path,m))
        df_csv_append = df_csv_append.append(df, ignore_index=True)
        df_csv_append.to_csv(merged_data_path)


   



#merge
data_path = "F:\Graduation Project\Gene\Final_Final_Adni1"
merge_data_path = "F:\Graduation Project\Gene\Final_Final_Final_Adni1\Gene_Data_Adni_1.csv"
merge(data_path ,merge_data_path)


