import os
import matplotlib.pyplot as plt
import numpy as np
import nibabel as nib
from tqdm import tqdm
import cv2
from scipy import ndimage
import SimpleITK as sitk
from keras.models import load_model 
#from nipype.interfaces import fsl
#from nipype.testing import example_data


def get_image_name(filename): #for keeping filename regardless extension 
    print  (filename.rsplit('.', 1)[0].lower())
    return filename.rsplit('.', 1)[0].lower() 

def maxProbability(arr):
    
    array=arr[0]
    max = array[0]
    for i in range(1,3):
        if array[i] > max:
            max = array[i]
    return max

def max_of_three_indices(array_label):
    
    max_item = array_label[0]
    max_index = 0
    for i in range(1,len(array_label)):
        if array_label[i] > max_item:
            max_item = array_label[i]
            max_index = i
            
    return max_index,max_item

def get_label(index):
    
    if index == 0:
        return 'AD'
    if index == 1:
        return 'CN'
    if index == 2:
        return 'MCI'
    

def get_average_label(iteration_loop,index_label,pred_proba_axial,pred_proba_coronal,pred_proba_sagittal):
    
    proba_axial = pred_proba_axial[iteration_loop][index_label]
    proba_coronal = pred_proba_coronal[iteration_loop][index_label]
    proba_sagittal = pred_proba_sagittal[iteration_loop][index_label]
    
    label_proba = (proba_axial + proba_coronal + proba_sagittal)/3
    return label_proba

def vote(pred_proba_axial,pred_proba_coronal,pred_proba_sagittal):
    
    predict_voting = []
    for i in range (len(pred_proba_axial)):
        array_label = []
        AD_label_proba = get_average_label(i,0,pred_proba_axial,pred_proba_coronal,pred_proba_sagittal)
        CN_label_proba = get_average_label(i,1,pred_proba_axial,pred_proba_coronal,pred_proba_sagittal)
        MCI_label_proba = get_average_label(i,2,pred_proba_axial,pred_proba_coronal,pred_proba_sagittal)
        array_label.append(AD_label_proba)
        array_label.append(CN_label_proba)
        array_label.append(MCI_label_proba)
    
        max_index,max_probability= max_of_three_indices(array_label)
        predict_voting.append(max_index)
        
    return predict_voting,max_probability,array_label

def predict_label_model(model,image_view):

    result= model.predict(image_view)
    result_label=np.argmax(result,axis=1)
    probability= round((maxProbability(result)*100),2)
    return result_label,result,probability

def predict_label_all_models (image_array_sagittal,image_array_coronal,image_array_axial):

    #load models
    sagittal_model = load_model('F:/Graduation Project/Flask/Models/model_sagittal.h5')
    coronal_model= load_model('F:/Graduation Project/Flask/Models/model_coronal.h5')
    axial_model = load_model('F:/Graduation Project/Flask/Models/model_axial.h5')

    #predict
    sagittal_label,all_probability_sagittal,probability_sagittal = predict_label_model(sagittal_model,image_array_sagittal)
    coronal_label,all_probability_coronal,probability_coronal = predict_label_model(coronal_model,image_array_coronal)
    axial_label,all_probability_axial,probability_axial = predict_label_model(axial_model,image_array_axial)

    #get label with maximum probability across the three models
    predict_voting,max_probability,all_probabilities = vote(all_probability_axial,all_probability_coronal,all_probability_sagittal)

    return get_label(sagittal_label[0]),probability_sagittal,get_label(coronal_label[0]),probability_coronal,get_label(axial_label[0]),probability_axial,get_label(predict_voting[0]), all_probabilities

def Append_image_resize(segments_folder,filename):
    image_array_sagittal=[]
    image_array_coronal=[]
    image_array_axial=[]
    image_size=224
    
    for m in tqdm(os.listdir(segments_folder)):
        image=cv2.imread(os.path.join(segments_folder,m))
        image=cv2.resize(image,(image_size,image_size))
        if (m == "Sagittal " + get_image_name(filename)+".png"):
            image_array_sagittal.append(image)
        elif (m == "Coronal " + get_image_name(filename)+".png"):
            image_array_coronal.append(image)
        elif (m == "Axial " + get_image_name(filename)+".png"):
            image_array_axial.append(image)
    image_array_sagittal = np.array(image_array_sagittal)
    image_array_coronal = np.array(image_array_coronal)
    image_array_axial = np.array(image_array_axial)

    result_sagittal_label,probability_sagittal,result_coronal_label,probability_coronal,result_axial_label,probability_axial,final_label,all_probabilities = predict_label_all_models(image_array_sagittal,image_array_coronal,image_array_axial)
    return result_sagittal_label,probability_sagittal,result_coronal_label,probability_coronal,result_axial_label,probability_axial,final_label,all_probabilities

def RGB_Segmentation(skull_stripped_folder,filename):
    #load images
    imageArray = []
    newimg = nib.load(os.path.join(skull_stripped_folder,filename))
    data = newimg.get_fdata()
    imageArray.append(data)
    imageArray = np.array(imageArray)

    #transform into rgb
    maindata=np.stack([imageArray]*3, axis=-1)

    imageArray_afterClipping = []
    for i in range(len(maindata)):
        maxValue = np.amax(maindata[i])
        minValue = np.amin(maindata[i])
        maindata_clipped= maindata[i]/np.amax(maindata[i])
        maindata_clipped = np.clip(maindata_clipped, 0, 1)
        imageArray_afterClipping.append(maindata_clipped)

    imageArray_afterClipping=np.array(imageArray_afterClipping)

   #convert image into 3 views and save it
    #segments_dst_path = '/home/farah/Documents/softwareApp/segments/'
    #segments_dst_path = 'F:/Graduation Project/Flask/Segments/'
    segments_dst_path = 'F:/Graduation Project/Flask/static/Segments/'

    for i in range(len(imageArray_afterClipping)):
        plt.switch_backend('agg')
        for j in range(3):
            if j == 0:
                rotated_img = ndimage.rotate(imageArray_afterClipping[i][imageArray_afterClipping.shape[1]//2, :,:], 180)
                plt.imshow(rotated_img)
                img_name = "Axial " + get_image_name(filename)
                plt.axis('off')
                plt.savefig(os.path.join(segments_dst_path,img_name),orientation = 'portrait',transparent = True, bbox_inches = 'tight',pad_inches=0)
                #plt.show()

            if j == 1:
                rotated_img = ndimage.rotate(imageArray_afterClipping[i][:,imageArray_afterClipping.shape[2]//2, :], 360)
                plt.imshow(rotated_img)
                img_name = "Coronal "+ get_image_name(filename)
                plt.axis('off')
                plt.savefig(os.path.join(segments_dst_path,img_name),orientation = 'portrait',transparent = True, bbox_inches = 'tight',pad_inches=0)
                #plt.show()

            if j == 2:
                rotated_img = ndimage.rotate(imageArray_afterClipping[i][:, :,imageArray_afterClipping.shape[3]//2],360)
                plt.imshow(rotated_img)
                img_name = "Sagittal "+ get_image_name(filename)
                plt.axis('off')
                plt.savefig(os.path.join(segments_dst_path,img_name),orientation = 'portrait',transparent = True, bbox_inches = 'tight',pad_inches=0)
                #plt.show()

    result_sagittal_label,probability_sagittal,result_coronal_label,probability_coronal,result_axial_label,probability_axial,final_label,all_probabilities = Append_image_resize(segments_dst_path,filename)
    return result_sagittal_label,probability_sagittal,result_coronal_label,probability_coronal,result_axial_label,probability_axial,final_label,all_probabilities

'''def skull_strip_nii(input_file, output_file, frac=0.3):
    
    btr = fsl.BET() #FSL brain extraction tool, BET , deal with nii files
    btr.inputs.in_file = input_file
    btr.inputs.frac = frac
    btr.inputs.out_file = output_file
    btr.cmdline
    result = btr.run()


def apply_skull_stripping(registration_folder_path, filename):
    
    destination_images_skullstripping="/home/farah/Documents/softwareApp/skullstripped_images/"
    skull_strip_nii((os.path.join(registration_folder_path,filename)),(os.path.join(destination_images_skullstripping,filename)),frac=0.35)
    result_sagittal_label,probability_sagittal,result_coronal_label,probability_coronal,result_axial_label,probability_axial,final_label,all_probabilities = RGB_Segmentation(destination_images_skullstripping,filename)
    return result_sagittal_label,probability_sagittal,result_coronal_label,probability_coronal,result_axial_label,probability_axial,final_label,all_probabilities


def registration(src_path, dst_path, ref_path, dst_path_mat):

    flt = fsl.FLIRT(bins=256, cost_func='corratio')
    flt.inputs.in_file = src_path
    flt.inputs.reference = ref_path
    flt.inputs.out_file = dst_path
    flt.inputs.out_matrix_file = dst_path_mat
    flt.cmdline
    res = flt.run()

    # command = ["/usr/local/fsl/bin/flirt", "-in", src_path, "-ref", ref_path, "-o", dst_path,
    #            "-bins", "256", "-cost", "corratio", "-searchrx", "0", "0",
    #            "-searchry", "0", "0", "-searchrz", "0", "0", "-dof", "12",
    #            "-interp", "spline"]
    # return_code = subprocess.call(command, stdout=open(os.devnull, "r"),stderr=subprocess.STDOUT)

    # if return_code == 0:
    #     print("Registration successful")
    # else:
    #     print("Registration failed with return code:", return_code)

    # return
    

def apply_registration(normalized_folder_path,filename):

    image_registeration_folder = "/home/farah/Documents/softwareApp/registered_images"
    ref_image_R="/home/farah/Documents/softwareApp/ref_img/intermediateADNI_098_S_0149_MR_MPR__GradWarp__B1_Correction__N3__Scaled_Br_20080206083054086_S11021_I89429.nii"
    dst_path_mat = "/home/farah/Documents/softwareApp/flirt_mat"
    matrix_file = get_image_name(filename)  + "_flirt.mat"
    
    registration((os.path.join(normalized_folder_path,filename)),os.path.join(image_registeration_folder,filename),ref_image_R,(os.path.join(dst_path_mat,matrix_file)))
    print((os.path.join(normalized_folder_path,filename)))
    print((os.path.join(image_registeration_folder,filename)))
    result_sagittal_label,probability_sagittal,result_coronal_label,probability_coronal,result_axial_label,probability_axial,final_label,all_probabilities = apply_skull_stripping(image_registeration_folder, filename)
    return result_sagittal_label,probability_sagittal,result_coronal_label,probability_coronal,result_axial_label,probability_axial,final_label,all_probabilities'''

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

    resample.SetOutputDirection(out_direction) #direction cosine matrix !!!
    resample.SetOutputOrigin(out_origin) #origin of the axis x,y,z
    resample.SetTransform(sitk.Transform()) 
    resample.SetDefaultPixelValue(image_sitk.GetPixelIDValue()) #setting pixels ID's 
    resample.SetInterpolator(sitk.sitkBSpline) #interpolation,sitk chose BSpline as it gives higher order of interpolation rather than linear

    return resample.Execute(image_sitk)

def Normalization(UPLOAD_FOLDER,filename):
    
    #normalize_folder = "/home/farah/Documents/softwareApp/normalized_images/"
    normalize_folder = "F:/Graduation Project/Flask/Normalized_Images/"

    ##loading data and transforming it into numpy array
    images_array_N=[]
    sitk_image_N = sitk.ReadImage(os.path.join(UPLOAD_FOLDER,filename))
    images_array_N.append( sitk.GetArrayFromImage(sitk_image_N))

    #Normalization
    resArray_N=[]
    actual_image_N = sitk.GetImageFromArray(images_array_N[0])
    res_N = resample_img(actual_image_N)
    resArray_N.append(sitk.GetArrayFromImage(res_N))

    #loading array images into files of .nii images
    convertImages_N = []
    nift_fileImgs_N=[]
    #from numpy array to nii images and save them to an external intermediate files 
    convertImages_N.append(np.array(resArray_N[0] , dtype=np.float32))
    nift_fileImgs_N.append(nib.Nifti1Image(convertImages_N[0],affine = np.eye(4)))
    nib.save(nift_fileImgs_N[0], normalize_folder + filename)
    print(filename)
    #result_sagittal_label,probability_sagittal,result_coronal_label,probability_coronal,result_axial_label,probability_axial,final_label,all_probabilities = apply_registration(normalize_folder,filename)
    #return result_sagittal_label,probability_sagittal,result_coronal_label,probability_coronal,result_axial_label,probability_axial,final_label,all_probabilities
    result_sagittal_label,probability_sagittal,result_coronal_label,probability_coronal,result_axial_label,probability_axial,final_label,all_probabilities= RGB_Segmentation(normalize_folder,filename)
    return result_sagittal_label,probability_sagittal,result_coronal_label,probability_coronal,result_axial_label,probability_axial,final_label,all_probabilities


