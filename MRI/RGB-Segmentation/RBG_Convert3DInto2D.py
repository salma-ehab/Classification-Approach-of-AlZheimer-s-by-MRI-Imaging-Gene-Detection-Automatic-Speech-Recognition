import matplotlib.pyplot as plt
import numpy as np
import nibabel as nib
from tqdm import tqdm
import os
from scipy import ndimage

#load images
imageArray = []
srcPath='D:\Graduation Project\Skull Stripped Data CN 4'
for m in tqdm(os.listdir(srcPath)):
    newimg = nib.load(os.path.join(srcPath,m))
    data = newimg.get_fdata()
    imageArray.append(data)
imageArray = np.array(imageArray)
print("The image array shape is",imageArray.shape)

#transform into rgb
maindata=np.stack([imageArray]*3, axis=-1)
print("The image array shape after adding rgb channels is",maindata.shape)

imageArray_afterClipping = []
print("The length of the array is",len(maindata))
for i in range(len(maindata)):
    maxValue = np.amax(maindata[i])
    minValue = np.amin(maindata[i])
    print("The maximum value is",maxValue)
    print("The minimum value is",minValue)
    maindata_clipped= maindata[i]/np.amax(maindata[i])
    maindata_clipped = np.clip(maindata_clipped, 0, 1)
    imageArray_afterClipping.append(maindata_clipped)

imageArray_afterClipping=np.array(imageArray_afterClipping)
print("The image array shape after clipping is",imageArray_afterClipping.shape)

#convert image into 3 views and save it
dst_path = 'D:\Graduation Project\CN Image Views'

for i in range(len(imageArray_afterClipping)):
    for j in range(3):
        if j == 0:
            rotated_img = ndimage.rotate(imageArray_afterClipping[i][imageArray_afterClipping.shape[1]//2, :,:], 270)
            plt.imshow(rotated_img)
            img_name = "image "+str(i + 75)+' sagittal'
            plt.axis('off')
            plt.savefig(os.path.join(dst_path,img_name),orientation = 'portrait',transparent = True, bbox_inches = 'tight',pad_inches=0)
            plt.show()

        if j == 1:
            rotated_img = ndimage.rotate(imageArray_afterClipping[i][:,imageArray_afterClipping.shape[2]//2, :], 270)
            plt.imshow(rotated_img)
            img_name = "image "+str(i + 75)+' coronal'
            plt.axis('off')
            plt.savefig(os.path.join(dst_path,img_name),orientation = 'portrait',transparent = True, bbox_inches = 'tight',pad_inches=0)
            plt.show()

        if j == 2:
            rotated_img = ndimage.rotate(imageArray_afterClipping[i][:, :,imageArray_afterClipping.shape[3]//2],90)
            plt.imshow(rotated_img)
            img_name = "image "+str(i + 75)+' axial'
            plt.axis('off')
            plt.savefig(os.path.join(dst_path,img_name),orientation = 'portrait',transparent = True, bbox_inches = 'tight',pad_inches=0)
            plt.show()
























