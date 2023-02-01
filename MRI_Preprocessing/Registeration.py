import os
import SimpleITK as sitk 
from tqdm import tqdm
import subprocess 
#import visualization
import matplotlib.pyplot as plt

def registration(src_path, dst_path, ref_path):
    command = ["flirt", "-in", src_path, "-ref", ref_path, "-out", dst_path,
               "-bins", "256", "-cost", "corratio", "-searchrx", "0", "0",
               "-searchry", "0", "0", "-searchrz", "0", "0", "-dof", "12",
               "-interp", "spline"]
    subprocess.call(command, stdout=open(os.devnull, "r"),
    stderr=subprocess.STDOUT)
    return


image_Registeration="/home/farah23/Downloads/MRI-APP/intermediateIMAGES_3/"
destination_images_R="/home/farah23/Downloads/MRI-APP/OutputReg_3/"
ref_image_R="/home/farah23/Downloads/intermediatefileADNI_098_S_0149_MR_MPR__GradWarp__B1_Correction__N3__Scaled_Br_20080206083054086_S11021_I89429.nii"
#images_array_R=[]

# sitk_image_ref_R= sitk.ReadImage(ref_image_R)  
# ref_show_R = sitk.GetArrayFromImage(sitk_image_ref_R)
# #plt.imshow(ref_show_R[110], cmap="gray")
# #plt.show()

for m in tqdm(os.listdir(image_Registeration)):
    registration((os.path.join(image_Registeration,m)),(os.path.join(destination_images_R,m)),ref_image_R)
    #sitk_image_R= sitk.ReadImage(os.path.join(destination_images_R,m))
    ###images_array_R.append( sitk.GetArrayFromImage(sitk_image_R))

#visualization.multi_slice_viewer(images_array2[0])
#plt.show()

#visualization.GRID(images_array2, 110, 2,5,10)d