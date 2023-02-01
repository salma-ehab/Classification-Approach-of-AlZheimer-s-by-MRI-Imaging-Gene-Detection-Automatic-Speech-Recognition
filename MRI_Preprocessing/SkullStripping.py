import os
import SimpleITK as sitk 
from tqdm import tqdm
import subprocess 
from nipype.interfaces import fsl
##import visualization

def skull_strip_nii(input_file, output_file, frac=0.3):
    
    btr = fsl.BET() #FSL brain extraction tool, BET , deal with nii files
    btr.inputs.in_file = input_file
    btr.inputs.frac = frac
    btr.inputs.out_file = output_file
    btr.cmdline
    result = btr.run()


#FSL brain extraction tool, BET , deal

image_skullstrip="/home/farah23/Downloads/MRI-APP/OutputReg_3/"
destination_images_skullstripping="/home/farah23/Downloads/MRI-APP/OutputSkullStripping_3/"
#images_array_S=[]
for m in tqdm(os.listdir(image_skullstrip)):
    skull_strip_nii((os.path.join(image_skullstrip,m)),(os.path.join(destination_images_skullstripping,m)),frac=0.35)
    #sitk_image_S= sitk.ReadImage(os.path.join(destination_images_skullstripping,m))
    #images_array_S.append( sitk.GetArrayFromImage(sitk_image_S))

#visualization.GRID(images_array_S, 110, 2,5,10)

#visualization.multi_slice_viewer(images_array2[0])
#plt.show()