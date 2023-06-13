import pandas as pd
import numpy as np
from tqdm import tqdm
import os
import joblib
import MRI

def get_max(list):
     
     max = list[0]
     index = 0
     for i in range(1,len(list)):
          if list[i] > max:
               max = list[i]
               index = i
     return index,max

def classify_AD_MCI_Gene(Gene_UPLOAD_FOLDER,Gene_filename):
     
     csv_file= pd.read_csv(os.path.join(Gene_UPLOAD_FOLDER,Gene_filename)).drop(["Unnamed: 0"], axis=1)
     gender_dict = {"m": 1, "f": 2} 
     csv_file['gender'] = csv_file['gender'].map(gender_dict) 
     features =  csv_file.iloc[:, 1:]

     rf_2 = joblib.load("F:/Graduation Project/Flask/Classifiers/rf_2.pkl")
     probability_array = rf_2.predict_proba(features)

     return probability_array


def combine(probabilities_MRI,probabilities_Genes_shown,probabilities_gene_max_result_1,gene_label,Gene_UPLOAD_FOLDER,Gene_filename):

    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(probabilities_MRI)
    print(probabilities_Genes_shown)
    print(probabilities_gene_max_result_1)


    if len(probabilities_MRI) == 0 and gene_label == "":
         return 0,0
    
    if len(probabilities_MRI) == 0:
         return gene_label,probabilities_Genes_shown
    
    if gene_label =="":
         index,max = get_max(probabilities_MRI)
         return MRI.get_label(index),max


    model_1_accuracy = 86.67
    model_2_accuracy = (73.17 + 68.7) /2

    model_1_weight =  round(model_1_accuracy /(model_1_accuracy + model_2_accuracy),2)
    model_2_weight =  round(model_2_accuracy /(model_1_accuracy + model_2_accuracy),2)

    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(model_1_weight)
    print(model_2_weight)

    if gene_label == "CN":
         probability_label_CN_model_2 = probabilities_gene_max_result_1
         probability_label_AD_MCI_model_2 = 1 - probabilities_gene_max_result_1

    elif gene_label =="AD" or gene_label =="MCI":
         probability_label_CN_model_2 = 1- probabilities_gene_max_result_1
         probability_label_AD_MCI_model_2 = probabilities_gene_max_result_1

    combined_CN = (probabilities_MRI[1]*model_1_weight) + (probability_label_CN_model_2 * model_2_weight)
    combined_AD_MCI = ((probabilities_MRI[0] + probabilities_MRI[2]) * model_1_weight) + (probability_label_AD_MCI_model_2 * model_2_weight)

    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(combined_CN)
    print(combined_AD_MCI)
    
    if combined_CN > combined_AD_MCI:
         final_label = "CN"
         final_label_probability=combined_CN

    else:
         new_AD_probability_model_1 = probabilities_MRI[0] / (probabilities_MRI[0] + probabilities_MRI[2])
         new_MCI_probability_model_1 = probabilities_MRI[2] / (probabilities_MRI[0] + probabilities_MRI[2])

         print("++++++++++++++++++++++++++++++++++++++++++++++++++++++")
         print(new_AD_probability_model_1)
         print(new_MCI_probability_model_1)

         if gene_label == "AD":
              probability_label_AD_model_2 = probabilities_Genes_shown
              probability_label_MCI_model_2 = 1-probabilities_Genes_shown
        
         elif gene_label == "MCI":
              probability_label_AD_model_2 = 1- probabilities_Genes_shown
              probability_label_MCI_model_2 = probabilities_Genes_shown

         elif gene_label == "CN":
              
              probability_array_AD_MCI = classify_AD_MCI_Gene(Gene_UPLOAD_FOLDER,Gene_filename)

              print("++++++++++++++++++++++++++++++++++++++++++++++++++++++")
              print(probability_array_AD_MCI)
         
              probability_label_AD_model_2 = probability_array_AD_MCI[0][1]
              probability_label_MCI_model_2 = probability_array_AD_MCI[0][0]

              print("++++++++++++++++++++++++++++++++++++++++++++++++++++++")
              print(probability_label_AD_model_2)
              print(probability_label_MCI_model_2)

         combined_AD = (new_AD_probability_model_1 * model_1_weight) + (probability_label_AD_model_2 * model_2_weight)
         combined_MCI = (new_MCI_probability_model_1 * model_1_weight) + (probability_label_MCI_model_2 * model_2_weight)

         print("++++++++++++++++++++++++++++++++++++++++++++++++++++++")
         print(combined_AD)
         print(combined_MCI)

         if combined_AD > combined_MCI:
              final_label = "AD"
              final_label_probability=combined_AD

         else:
              final_label = "MCI"
              final_label_probability=combined_MCI

    return final_label,final_label_probability
              

              
         
         

         

    
        



    



