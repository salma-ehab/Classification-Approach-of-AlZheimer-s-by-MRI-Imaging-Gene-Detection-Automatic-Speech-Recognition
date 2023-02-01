import numpy as np
import SimpleITK as sitk 
#import visualization
from tqdm import tqdm 
import os 
import nibabel as nib


def resample_img(image_sitk, out_spacing=[1.0, 1.0, 1.0], out_direction= (1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0), out_origin=[0,0,0]):

    original_spacing = image_sitk.GetSpacing()
    original_size = image_sitk.GetSize()


    out_size = [
        int(np.round(original_size[0] * (original_spacing[0] / out_spacing[0]))),
        int(np.round(original_size[1] * (original_spacing[1] / out_spacing[1]))),
        int(np.round(original_size[2] * (original_spacing[2] / out_spacing[2])))]
    
    resample = sitk.ResampleImageFilter() #object 
    resample.SetOutputSpacing(out_spacing) #spacing between voxels of 3d images
    resample.SetSize(out_size) 

    resample.SetOutputDirection(out_direction) #direction cosin matrix !!!
    resample.SetOutputOrigin(out_origin) #origin of the axis x,y,z
    resample.SetTransform(sitk.Transform()) #!!!
    resample.SetDefaultPixelValue(image_sitk.GetPixelIDValue()) #setting pixels ID's 
    resample.SetInterpolator(sitk.sitkBSpline) #interpolation:!!!! ,sitk chose BSpline as it gives higher order of interpolation rather than linear

    return resample.Execute(image_sitk)


##loading data and transforming it into numpy array
image_path_N="/home/farah23/Downloads/Images_300_1"
images_array_N=[]
image_array_names_N=[]
for m in tqdm(os.listdir(image_path_N)):
    sitk_image_N = sitk.ReadImage(os.path.join(image_path_N,m))
    images_array_N.append( sitk.GetArrayFromImage(sitk_image_N))
    image_array_names_N.append(m)


##Normalization
resArray_N=[]
for i in range (200) : 
    actual_image_N = sitk.GetImageFromArray(images_array_N[i])
    res_N = resample_img(actual_image_N)
    resArray_N.append(sitk.GetArrayFromImage(res_N))
    #multi_slice_viewer(resArray[i])
    #plt.show() 

#visualization.GRID(resArray, 110, 2,5,10)

#loading array images into files of .nii images
convertImages_N = []
nift_fileImgs_N=[]
#from numpy array to nii images and save them to an external intermediate files 
for i in range (200) : 
     convertImages_N.append(np.array(resArray_N[i] , dtype=np.float32))
     nift_fileImgs_N.append(nib.Nifti1Image(convertImages_N[i],affine = np.eye(4)))
     nib.save(nift_fileImgs_N[i], "/home/farah23/Downloads/MRI-APP/intermediateIMAGES_/intermediatefile" + image_array_names_N[i])
    
