import pandas as pd
import numpy as np
from tqdm import tqdm
import os
import joblib

def max_of_three_indices(array_label):
    
    max_item = array_label[0]
    max_index = 0
    for i in range(1,len(array_label)):
        if array_label[i] > max_item:
            max_item = array_label[i]
            max_index = i
            
    return max_index,max_item

def get_average_label(iteration_loop,index_label,pred_proba_svr,pred_proba_rf):
    
    proba_svr = pred_proba_svr[iteration_loop][index_label]
    proba_rf= pred_proba_rf[iteration_loop][index_label]
    
    label_proba = (proba_svr + proba_rf)/2
    return label_proba

def voting(proba_label_svr,proba_label_rf):
    
    predict_voting = []
    for i in range (len(proba_label_svr)):
        array_label = []
        CN_label_proba = get_average_label(i,0,proba_label_svr,proba_label_rf)
        AD_MCI_label_proba = get_average_label(i,1,proba_label_svr,proba_label_rf)
        array_label.append(CN_label_proba)
        array_label.append(AD_MCI_label_proba)
        max_index,max_item = max_of_three_indices(array_label)
        predict_voting.append(max_index)
    

    return predict_voting,max_item

def predict_label(classifier,data,type_of_classifier):

    pred_label=classifier.predict(data) 

    if type_of_classifier == 0:
        probability_array = []
        if pred_label[0] < 0.5:
            pred_label = 0
        else:
            pred_label = 1
        
        one_label_probability_array = []
        distance = abs(pred_label - 0.5) - classifier.epsilon
        proba = 1 / (1 + np.exp(-distance))

        if  pred_label == 0:
            one_label_probability_array.append(proba)
            one_label_probability_array.append(1-proba)
        
        elif  pred_label == 1:
            one_label_probability_array.append(1-proba)
            one_label_probability_array.append(proba)
        
        probability_array.append(one_label_probability_array)

    elif type_of_classifier == 1:
         probability_array = classifier.predict_proba(data)


    return pred_label,probability_array

def classify(upload_folder,file_name):

     csv_file= pd.read_csv(os.path.join(upload_folder,file_name)).drop(["Unnamed: 0"], axis=1)
     gender_dict = {"m": 1, "f": 2} 
     csv_file['gender'] = csv_file['gender'].map(gender_dict) 
     features =  csv_file.iloc[:, 1:]

     svr_1 = joblib.load("F:/Graduation Project/Flask/Classifiers/svr_1.pkl")
     rf_1 = joblib.load("F:/Graduation Project/Flask/Classifiers/rf_1.pkl")
     rf_2 = joblib.load("F:/Graduation Project/Flask/Classifiers/rf_2.pkl")
    

     pred_label_svr_1,svr_1_probability_array = predict_label(svr_1,features,0)
     pred_label_rf_1,rf_1_probability_array= predict_label(rf_1,features,1)

     print("The list of probabilities as predicted by SVR in first step of Gene approach:",svr_1_probability_array)
     print("The list of probabilities as predicted by RF in first step of Gene approach:",rf_1_probability_array)

     predict_voting_1,result_probability_1 = voting(svr_1_probability_array,rf_1_probability_array)


     print("The label chosen by first step of Gene approach:",predict_voting_1[0])
     print("The probability of the label chosen by first step of Gene approach:",result_probability_1)

     

     array_probabilities = []
     
     if predict_voting_1[0] == 1:
         
         pred_label_rf_2,rf_2_probability_array = predict_label(rf_2,features,1)
         probability_2 = rf_2_probability_array[0][pred_label_rf_2[0]]

         print("The label chosen by second step of Gene approach:",pred_label_rf_2[0])
         print("The probability of the label chosen by second step of Gene approach:",probability_2)

         
         
         max_result_probability_2 = (result_probability_1)*(probability_2/(probability_2+(1-probability_2)))
         min_result_probability_2 = (result_probability_1)*((1-probability_2)/(probability_2+(1-probability_2)))

         print("The probability of the label chosen by second step of Gene approach given that class AD_MCI was chosen in first step:",max_result_probability_2)
         print("The probability of the label not chosen by second step of Gene approach given that class AD_MCI was chosen in first step:",min_result_probability_2)


         if pred_label_rf_2[0] == 0:
             
             array_probabilities.append(min_result_probability_2)
             array_probabilities.append(1-result_probability_1)
             array_probabilities.append(max_result_probability_2)

             print("The list of probabilities as predicted by Gene approach:",array_probabilities)

             return "MCI",array_probabilities
         
         elif pred_label_rf_2[0] == 1:
             
             array_probabilities.append(max_result_probability_2)
             array_probabilities.append(1-result_probability_1)
             array_probabilities.append(min_result_probability_2)

             print("The list of probabilities as predicted by Gene approach:",array_probabilities)

             return "AD",array_probabilities
    
     elif predict_voting_1[0] == 0:
         
         array_probabilities.append(1-result_probability_1)
         array_probabilities.append(result_probability_1)

         print("Probability of CN:",round(result_probability_1,2))
         print("Probability of AD-MCI:",round(1-result_probability_1,2))

         print("The list of probabilities as predicted by Gene approach:",array_probabilities)

         return "CN",array_probabilities
         

def add_age_gender(upload_folder,file_name,age,gender):
     
     csv_file= pd.read_csv(os.path.join(upload_folder,file_name))  
     csv_file['gender'] = gender  
     csv_file['age'] = age
     csv_file.to_csv(os.path.join(upload_folder,file_name))

     predicted_label,all_probabilities = classify(upload_folder,file_name)
     return predicted_label,all_probabilities
  
def transpose(upload_folder,file_name,age,gender):

     csv_file= pd.read_csv(os.path.join(upload_folder,file_name),index_col = 0)   
     csv_file= csv_file.set_index('SNP Name').T.reset_index()
     csv_file.to_csv(os.path.join(upload_folder,file_name),index=False)

     predicted_label,all_probabilities = add_age_gender(upload_folder,file_name,age,gender)
     return predicted_label,all_probabilities

def drop_unnecessary_columns(upload_folder,file_name,age,gender):

    df= pd.read_csv(os.path.join(upload_folder,file_name),index_col=0) 
    df.drop(['Unnamed: 0', 'Sample ID','Sample Index','GC Score','SNP Index','Allele1 - Top','Allele2 - Top','Allele1 - Forward',
    'Allele2 - Forward','Allele1 - AB','Allele2 - AB','Chr','Position','GT Score','Cluster Sep','SNP','Theta','R','X','Y','X Raw'
    ,'Y Raw','B Allele Freq','Log R Ratio','ref_allele'], axis=1,inplace=True)
    df.to_csv(os.path.join(upload_folder,file_name))

    predicted_label,all_probabilities = transpose(upload_folder,file_name,age,gender)
    return predicted_label,all_probabilities

def add_variation(upload_folder,file_name,age,gender):

    allele_1=[]
    allele_2=[]
    ref_allele=[]
    variation=[]

    df_allele_1= pd.read_csv(os.path.join(upload_folder,file_name), usecols = ['Allele1 - Forward'])
    df_array_allele_1 = df_allele_1.values
    for item in df_array_allele_1 :
        for inner_item in item:
            allele_1.append(inner_item)


    df_allele_2= pd.read_csv(os.path.join(upload_folder,file_name), usecols = ['Allele2 - Forward'])
    df_array_allele_2 = df_allele_2.values
    for item in df_array_allele_2 :
        for inner_item in item:
            allele_2.append(inner_item)

    df_ref_allele= pd.read_csv(os.path.join(upload_folder,file_name), usecols = ['ref_allele'])
    df_array_ref_allele = df_ref_allele.values
    for item in df_array_ref_allele :
        for inner_item in item:
            ref_allele.append(inner_item)

       
    for i in range(len(ref_allele)):
        if((ref_allele[i] == allele_1[i]) and (ref_allele[i] == allele_2[i])):
            variation.append(0)
            
        elif ((ref_allele[i] != allele_1[i]) and (ref_allele[i] == allele_2[i]) or ((ref_allele[i] == allele_1[i]) and (ref_allele[i] != allele_2[i]))):
            variation.append(1)

        elif ((ref_allele[i] != allele_1[i]) and (ref_allele[i] != allele_2[i])):
            variation.append(2)

    csv_file= pd.read_csv(os.path.join(upload_folder,file_name))    
    csv_file['allele_variation'] = variation
    csv_file.to_csv(os.path.join(upload_folder,file_name))

    predicted_label,all_probabilities = drop_unnecessary_columns(upload_folder,file_name,age,gender)
    return predicted_label,all_probabilities

def read_ref_allele_and_snp():

    csv_file = "F:/Graduation Project/Flask/Gene_Ref_Allele/S_002_S_0295.csv"
    ref_allele = []
    snp_array= []

    df_ref = pd.read_csv(csv_file, usecols = ['ref_allele'])                             
    ref_Array = df_ref.values 
    for item in  ref_Array:
        for inner_item in item:
            ref_allele.append(inner_item)

    df_snp = pd.read_csv(csv_file, usecols = ['SNP Name'])                             
    snp_names= df_snp.values 
    for item in  snp_names:
        for inner_item in item:
            snp_array.append(inner_item)

    return snp_array,ref_allele 

def add_ref_allele(upload_folder,file_name,age,gender):
     
     ref_allele_2 = []
     snp_array,ref_allele  = read_ref_allele_and_snp()

     snp_array_2= []
     df_csv_file= pd.read_csv(os.path.join(upload_folder,file_name), usecols = ['SNP Name'])
     df_snp = df_csv_file.values
     for item in  df_snp:
        for inner_item in item:
            snp_array_2.append(inner_item)

     for index in range(len(snp_array)):
         for index_2 in range(len(snp_array_2)):
             if snp_array[index] == snp_array_2[index_2]:
                  ref_allele_2.append(ref_allele[index])
                  break
             
     csv_file= pd.read_csv(os.path.join(upload_folder,file_name))    
     csv_file['ref_allele'] = ref_allele_2
     csv_file.to_csv(os.path.join(upload_folder,file_name))

     predicted_label,all_probabilities = add_variation(upload_folder,file_name,age,gender)
     return predicted_label,all_probabilities

def filtering(upload_folder,file_name,age,gender):
        
        df = pd.read_csv(os.path.join(upload_folder,file_name))
        snp_name = df['SNP Name'].astype(str)
        filtered_chr_snp_geneLocation = df[(df['Chr'] != '1') & (df['Chr'] != '14') & (df['Chr'] != '19') & (df['Chr'] != '21') | (~snp_name.str.startswith('rs')) 
        | ((df['Chr'] == '19') & ((df['Position']<50090879) | (df['Position']>50114490))) | ((df['Chr'] == '14') & ((df['Position']<72662932) | (df['Position']>72766862)))
        | ((df['Chr'] == '1') & ((df['Position']<225114896) | (df['Position']>225160427))) | ((df['Chr'] == '21') & ((df['Position']<26164732) | (df['Position']>26475003)))].index
        df.drop(filtered_chr_snp_geneLocation, inplace=True)
        df.to_csv(os.path.join(upload_folder,file_name), index=False)

        predicted_label,all_probabilities= add_ref_allele(upload_folder,file_name,age,gender)
        return predicted_label,all_probabilities







