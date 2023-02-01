import pandas as pd
from tqdm import tqdm
import os
import shutil

srcImagesPath = "/home/farah23/Downloads/MRI-APP/OutputSkullStripping_3/"
dstImagesPath = "/home/farah23/Downloads/MRI-APP/LabellingOutput"

df = pd.read_csv("/home/farah23/Downloads/ADNI1_Screening_1.5T_12_08_2022.csv", usecols = ['Subject', 'Group'])        
df_dtypes = df.infer_objects()                         
CSVArray = df.values 

for m in tqdm(os.listdir(srcImagesPath)):
    ImageNameSplitted = m.split("_")
    ImageID = ImageNameSplitted[1]+"_"+ImageNameSplitted[2]+"_"+ImageNameSplitted[3]
    for item in CSVArray:
        if (ImageID == item[0]):
            shutil.move(os.path.join(srcImagesPath,m), os.path.join(dstImagesPath,item[1]))
            break