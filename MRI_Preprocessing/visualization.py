import os
from pathlib import Path
import cv2
import matplotlib.pyplot as plt
import nibabel as nib
import numpy as np
from matplotlib.axes import Axes
from matplotlib.backend_bases import MouseButton
from tqdm import tqdm
#import imageio 
from skimage import io  
import SimpleITK as sitk 
import imageio
from nipype.interfaces import fsl
import subprocess 

def process_key(event):
    fig = event.canvas.figure
    ax = fig.axes[0]
    if event.key == 'a':
        previous_slice(ax)
    elif event.key == 'w':
        next_slice(ax)
    fig.canvas.draw()

def multi_slice_viewer(volume):
    #remove_keymap_conflicts({'j', 'k'})
    fig, ax = plt.subplots()
    ax.volume = volume
    ax.index = 50  #arbitrary index of a slice 
    #ax.index=60
    #text=ax.text(0,0, "", va="bottom", ha="left")
    ax.imshow(volume[ax.index],cmap='gray')
    
    #plt.imshow(volume[0:ax.index, 0:ax.index],cmap='gray')
    #ax.index = volume.shape[2] 
    #ax.imshow(volume[:,:,0])
    cid = fig.canvas.mpl_connect('key_press_event', process_key)
       
def onclick(event):
    
    fig = event.canvas.figure
    ax = fig.axes[0]
    #if event.button is MouseButton.LEFT:
        #previous_slice(ax)
    #elif event.button is MouseButton.RIGHT:
    next_slice(ax)
    cid3 = fig.canvas.draw() 
   
def previous_slice(ax):
    volume = ax.volume
    #ax.index = (ax.index - 1) % volume.shape[2]  # wrap around using %
    
    ax.index = (ax.index - 1) % volume.shape[0] # wrap around using % 
    ax.images[0].set_array(volume[ax.index])
    

def next_slice(ax):
    volume = ax.volume
   # ax.index = (ax.index + 1) % volume.shape[2]
    
    ax.index = (ax.index + 1) % volume.shape[0] 
    ax.images[0].set_array(volume[ax.index])

'''def bias_field_correction(src_path, dst_path):
    #n4 = N4BiasFieldCorrection()
    n4.inputs.input_image = src_path
    n4.inputs.output_image = dst_path
    n4.inputs.dimension = 3 #image dimensions 
    n4.inputs.n_iterations = [100, 100, 60, 40] #! multiscale optimization levels 4 scales for 4 res levels, each res level has limited iterations,number of iterations per resolution level to reach a specific resolution acc to length of array scales
    n4.inputs.shrink_factor = 4 #reduce size & complexity of image to reduce computation size <4
    n4.inputs.convergence_threshold = 1e-4 # threshold to avoid overfitting when comparing 2 images below threshold 
    n4.inputs.bspline_fitting_distance = 300 #!!
    n4.run()'''

def GRID(array, slc, row, col,iteration):
    ###3x3 grid view
    plt.figure(figsize=(10, 10))  
    for i in range(iteration):       
        ax = plt.subplot(row, col, i + 1)        
        plt.imshow(array[i][slc], cmap='gray')    #static images, not visualization of images by process keys.
        #plt.title(class_names[labels[i]])        
        plt.axis("off") 
    plt.show()

##########################################VISUALIZATION###########################################################
image_path_visu="/home/farah23/Downloads/ADNI-ALLIMAGES/"
images_array=[]
for m in tqdm(os.listdir(image_path)):
    sitk_image = sitk.ReadImage(os.path.join(image_path,m))
    images_array.append( sitk.GetArrayFromImage(sitk_image))

###3x3 grid view
#GRID(images_array,40)


##############################Bias correction ###############################################################
'''image_biased="/home/farah/Downloads/MRI-APP/outputIMAGES_skullstripping/"
destination_images_biased="/home/farah/Downloads/MRI-APP/outputIMAGES_bias/"
images_array4=[]
for m in tqdm(os.listdir(image_biased)):
    bias_field_correction((os.path.join(image_biased,m)),(os.path.join(destination_images_biased,m)))
    sitk_image4= sitk.ReadImage(os.path.join(destination_images_biased,m))
    images_array4.append( sitk.GetArrayFromImage(sitk_image4))'''

#GRID(images_array4,110)
