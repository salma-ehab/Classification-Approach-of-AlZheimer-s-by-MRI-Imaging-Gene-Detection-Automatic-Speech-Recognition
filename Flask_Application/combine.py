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

def get_weight_two_models(acc_model_1,acc_model_2):

    model_1_weight =  acc_model_1 /(acc_model_1 + acc_model_2)
    model_2_weight =  acc_model_2 /(acc_model_1 + acc_model_2)

    return model_1_weight,model_2_weight


def combine(probabilities_MRI,probabilities_Genes,probabilities_Audio):
    #model 1 --> mri
    #model 2 --> gene
    #model 3 --> audio
    
    #no diagnosis
    if len(probabilities_MRI) == 0 and len(probabilities_Genes) == 0 and len(probabilities_Audio) == 0:
         return 0,0
    
    #only mri diagnosis
    if len(probabilities_Genes) == 0 and len(probabilities_Audio) == 0:
         index,max = get_max(probabilities_MRI)
         return MRI.get_label(index),probabilities_MRI
    
    #only gene diagnosis
    if len(probabilities_MRI) == 0 and len(probabilities_Audio) == 0:
         index,max = get_max(probabilities_Genes)
         return MRI.get_label(index),probabilities_Genes
    
    #only audio diagnosis
    if len(probabilities_MRI) == 0 and len(probabilities_Genes) == 0:
         index,max = get_max(probabilities_Audio)
         return MRI.get_label(index),probabilities_Audio
    
    model_1_accuracy = 86.67
    model_2_accuracy = (73.17 + 68.7) /2
    model_3_accuracy = 85.71

    array_combined_probabilities = []

    #mri and gene diagnosis
    if len(probabilities_Audio) == 0:
          for i in range(len(probabilities_MRI)):
                model_1_weight,model_2_weight = get_weight_two_models(model_1_accuracy,model_2_accuracy)
                print("wwwww")
                print(model_1_weight)
                print(model_2_weight)
                array_combined_probabilities.append((model_1_weight*probabilities_MRI[i])+(model_2_weight*probabilities_Genes[i]))

    #mri and audio diagnosis
    if len(probabilities_Genes) == 0:
          for i in range(len(probabilities_MRI)):
                model_1_weight,model_3_weight = get_weight_two_models(model_1_accuracy,model_3_accuracy)
                print("wwwww")
                print(model_1_weight)
                print(model_3_weight)
                array_combined_probabilities.append((model_1_weight*probabilities_MRI[i])+(model_3_weight*probabilities_Audio[i]))

    #gene and audio diagnosis
    if len(probabilities_MRI) == 0:
          for i in range(len(probabilities_Genes)):
                model_2_weight,model_3_weight = get_weight_two_models(model_2_accuracy,model_3_accuracy)
                print("wwwww")
                print(model_2_weight)
                print(model_3_weight)
                array_combined_probabilities.append((model_2_weight*probabilities_Genes[i])+(model_3_weight*probabilities_Audio[i]))

    #mri, gene and audio diagnosis
    if len(probabilities_MRI) != 0 and len(probabilities_Genes) != 0 and len(probabilities_Audio) != 0:
         model_1_weight =  model_1_accuracy /(model_1_accuracy + model_2_accuracy+model_3_accuracy)
         model_2_weight =  model_2_accuracy /(model_1_accuracy + model_2_accuracy+model_3_accuracy)
         model_3_weight =  model_3_accuracy /(model_1_accuracy + model_2_accuracy+model_3_accuracy)
         print("wwwww")
         print(model_1_weight)
         print(model_2_weight)
         print(model_3_weight)
         for i in range(len(probabilities_MRI)):
              array_combined_probabilities.append((model_1_weight*probabilities_MRI[i]) +(model_2_weight*probabilities_Genes[i])+(model_3_weight*probabilities_Audio[i]))
         

    final_label,final_probability = get_max(array_combined_probabilities)
    final_label = MRI.get_label(final_label)

    print("CCCCCCCCCCCCCCCCCCCCCCCCCCCC")
    print(probabilities_MRI)
    print(probabilities_Audio)
    print(probabilities_Genes)
    print(array_combined_probabilities)
    return final_label,array_combined_probabilities


              
         
         

         

    
        



    



