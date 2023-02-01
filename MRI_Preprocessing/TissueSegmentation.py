#################################Tissue segmentation########################################################
import nibabel as nib
import numpy as np
##from sklearn.cluster import KMeans
from nipype.interfaces import fsl
import matplotlib.pyplot as plt
from tqdm import tqdm
import os
import subprocess 
import SimpleITK as sitk 
#import visualization


def fast(src_path, dst_path):
    command = ["fast", "-t", "2", "-n", "3", "-H", "0.3", "-I", "4", "-l", "20.0",
               "-o",dst_path, src_path] 
    
    subprocess.call(command, stdout=open(os.devnull), stderr=subprocess.STDOUT)
    return

#######################################################################################
source_dir_T="/home/farah23/Downloads/MRI-APP/LabellingOutput/MCI/"
dest_dir_T="/home/farah23/Downloads/MRI-APP/MCI_200_Output_TissueSeg/"
#images_array5=[]
for m in tqdm(os.listdir(source_dir_T)):
    fast((os.path.join(source_dir_T,m)),(os.path.join(dest_dir_T,m)))
    # for i in range(3):
    #     file=m.split(".nii.gz")
    #     newfile=file[0]
    #     sitk_image5= sitk.ReadImage(os.path.join(dest_dir,newfile +"_pve_" + str(i) + ".nii.gz"))
    #     images_array5.append( sitk.GetArrayFromImage(sitk_image5))

#visualization.GRID(images_array5, 110,3,3,9)