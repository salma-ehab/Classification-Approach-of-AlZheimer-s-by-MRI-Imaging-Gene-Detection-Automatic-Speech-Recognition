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


def combine(probabilities_MRI,probabilities_Genes,gene_predicted_label,probabilities_Audio):
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
         print(probabilities_Audio)
         return MRI.get_label(index),probabilities_Audio
    
    model_1_accuracy = 86.67
    model_2_accuracy = (73.17 + 68.7) /2
    model_3_accuracy = 82.9

    array_combined_probabilities = []

    #mri and gene diagnosis
    if len(probabilities_Audio) == 0:
           
           model_1_weight,model_2_weight = get_weight_two_models(model_1_accuracy,model_2_accuracy)

           print("wwwww")
           print(model_1_weight)
           print(model_2_weight)

           if gene_predicted_label =="CN":
                   array_combined_probabilities.append((model_1_weight*(probabilities_MRI[0]+probabilities_MRI[2])) +(model_2_weight*probabilities_Genes[0]))
                   array_combined_probabilities.append((model_1_weight*probabilities_MRI[1]) +(model_2_weight*probabilities_Genes[1]))

                   final_label,final_probability = get_max(array_combined_probabilities)
                   if final_label != 1:
                          index,max = get_max(probabilities_MRI)
                          return MRI.get_label(index),probabilities_MRI
                   else:
                         return "CN", array_combined_probabilities
           else:
               for i in range(len(probabilities_MRI)):
                   array_combined_probabilities.append((model_1_weight*probabilities_MRI[i])+(model_2_weight*probabilities_Genes[i]))
                   final_label,final_probability = get_max(array_combined_probabilities)
                   final_label = MRI.get_label(final_label)

                   print("AAAAAAAAAAAAAAAAAAA")
                   print(array_combined_probabilities)


               return final_label,array_combined_probabilities

    #mri and audio diagnosis
    if len(probabilities_Genes) == 0:
          for i in range(len(probabilities_MRI)):
                model_1_weight,model_3_weight = get_weight_two_models(model_1_accuracy,model_3_accuracy)
                print("wwwww")
                print(model_1_weight)
                print(model_3_weight)
                array_combined_probabilities.append((model_1_weight*probabilities_MRI[i])+(model_3_weight*probabilities_Audio[i]))
                final_label,final_probability = get_max(array_combined_probabilities)
                final_label = MRI.get_label(final_label)
          return final_label,array_combined_probabilities

    #gene and audio diagnosis
    if len(probabilities_MRI) == 0:
           
           model_2_weight,model_3_weight = get_weight_two_models(model_2_accuracy,model_3_accuracy)

           print("wwwww")
           print(model_2_weight)
           print(model_3_weight)

           if gene_predicted_label =="CN":
                   array_combined_probabilities.append((model_2_weight*probabilities_Genes[0])+(model_3_weight*(probabilities_Audio[0]+probabilities_Audio[2])))
                   array_combined_probabilities.append((model_2_weight*probabilities_Genes[1]) +(model_3_weight*probabilities_Audio[1]))

                   final_label,final_probability = get_max(array_combined_probabilities)
                   if final_label != 1:
                          index,max = get_max(probabilities_Audio)
                          return MRI.get_label(index),probabilities_Audio
                   else:
                         return "CN", array_combined_probabilities
           else:
               for i in range(len(probabilities_Genes)):
                   array_combined_probabilities.append((model_2_weight*probabilities_Genes[i])+(model_3_weight*probabilities_Audio[i]))
                   final_label,final_probability = get_max(array_combined_probabilities)
                   final_label = MRI.get_label(final_label)
               return final_label,array_combined_probabilities

    #mri, gene and audio diagnosis
    if len(probabilities_MRI) != 0 and len(probabilities_Genes) != 0 and len(probabilities_Audio) != 0:
         
         model_1_weight =  model_1_accuracy /(model_1_accuracy + model_2_accuracy+model_3_accuracy)
         model_2_weight =  model_2_accuracy /(model_1_accuracy + model_2_accuracy+model_3_accuracy)
         model_3_weight =  model_3_accuracy /(model_1_accuracy + model_2_accuracy+model_3_accuracy)

         print("wwwww")
         print(model_1_weight)
         print(model_2_weight)
         print(model_3_weight)
         
         if gene_predicted_label =="CN":
                array_combined_probabilities.append((model_1_weight*(probabilities_MRI[0]+probabilities_MRI[2])) +(model_2_weight*probabilities_Genes[0])+(model_3_weight*(probabilities_Audio[0]+probabilities_Audio[2])))
                array_combined_probabilities.append((model_1_weight*probabilities_MRI[1]) +(model_2_weight*probabilities_Genes[1])+(model_3_weight*probabilities_Audio[1]))

                print("LLLLLL")
                print(array_combined_probabilities)

                final_label,final_probability = get_max(array_combined_probabilities)
                if final_label != 1:
                          array_combined_probabilities = []
                          model_1_weight,model_3_weight = get_weight_two_models(model_1_accuracy,model_3_accuracy)
                          array_combined_probabilities.append((model_1_weight*probabilities_MRI[0]) + (model_3_weight*probabilities_Audio[0]))
                          array_combined_probabilities.append((model_1_weight*probabilities_MRI[1])+ (model_3_weight*probabilities_Audio[1]))
                          array_combined_probabilities.append((model_1_weight*probabilities_MRI[2]) +(model_3_weight*probabilities_Audio[2]))
                          final_label,final_probability = get_max(array_combined_probabilities)

                          if final_label == 0:
                                return "AD", array_combined_probabilities
                          else:
                                return "MCI", array_combined_probabilities
                          
                else :
                      return "CN", array_combined_probabilities    
                
         else :
               for i in range(len(probabilities_MRI)):
                     array_combined_probabilities.append((model_1_weight*probabilities_MRI[i]) +(model_2_weight*probabilities_Genes[i])+(model_3_weight*probabilities_Audio[i]))
                     final_label,final_probability = get_max(array_combined_probabilities)
                     final_label = MRI.get_label(final_label)
               return final_label,array_combined_probabilities


              
         
         

         

    
        



    



