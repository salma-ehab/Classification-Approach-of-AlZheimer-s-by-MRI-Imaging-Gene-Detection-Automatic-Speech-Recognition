from flask import Flask, render_template, request, session, redirect, flash, url_for
from werkzeug.utils import secure_filename
import os
from tqdm import tqdm
import MRI
import Gene
import Audio
import combine
import datetime

app = Flask(__name__)
#UPLOAD_FOLDER = '/home/farah/Documents/softwareApp/HistoryUploads'
MRI_UPLOAD_FOLDER = 'F:/Graduation Project/Flask/MRI_Uploads/'
Gene_UPLOAD_FOLDER = 'F:/Graduation Project/Flask/Gene_Uploads/'
Audio_UPLOAD_FOLDER ='F:/Graduation Project/Flask/Audio_Uploads/'
app.secret_key = "MRI-flask" #for browser cookies for security.
array_mri_extension = []
array_gene_extension = []
array_audio_extension = []
array_mri_extension.append(set(['nii']))
array_gene_extension.append(set(['csv']))
array_audio_extension.append(set(['mp3']))
array_audio_extension.append(set(['wav']))
array_audio_extension.append(set(['csv']))


Gene_predicted_label_1 = ""
Gene_pl=""
Gene_all_probabilities = []
Gene_AD_probability = 0
Gene_CN_probability = 0
Gene_MCI_probability = 0
Gene_AD_MCI_probability = 0

Audio_predicted_label = ""
Audio_all_probabilities = []
Audio_AD_probability = 0
Audio_CN_probability = 0
Audio_MCI_probability = 0


MRI_label=""
MRI_all_Probabilities = []
MRI_AD_probability = 0
MRI_CN_probability = 0
MRI_MCI_probability = 0

MRI_label_sagittal=""
MRI_probability_sagittal=0
MRI_label_coronal=""
MRI_probability_coronal=0
MRI_label_axial=""
MRI_probability_axial=0


sagittal_image = ""
coronal_image = ""
axial_image = ""

def allowed_file(filename,allowed_extensions): #boolean, for extensions
    flag = False
    for i in range(len(allowed_extensions)):
         if '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions[i]:
             flag = True
    return flag

def get_age(birth_year,birth_month,birth_day):

    today = datetime.date.today()
    current_year = today.year
    current_month = today.month
    current_day = today.day

    if birth_month > current_month:
           age = current_year - birth_year -1

    elif birth_month < current_month:
           age = current_year - birth_year

    
    elif birth_month == current_month:
           if birth_day > current_day:
                age = current_year - birth_year -1

           elif birth_day <= current_day:     
                age = current_year - birth_year

    return age

def get_label_probability(array_probability):
    
    AD_probability = array_probability[0]
    CN_probability = array_probability[1]
    MCI_probability = array_probability[2]

    return AD_probability,CN_probability,MCI_probability

        
def upload(file_name,upload_folder,allowed_extensions,empty_file_message,allowed_types_message,check_type):
     
     if file_name not in request.files: #dict. and check with key file1 to ensure that a file was indeed submitted in the request.

        if check_type == 0:
            return  redirect(url_for('Run_MRI'))
        
        elif check_type ==1:
            return redirect(url_for('Run_Gene'))
        
        elif check_type ==2:
            return redirect(url_for('Run_Audio'))
        
         
     file = request.files[file_name] #retrieve file with key file1
        
     if file.filename == '':
        flash(empty_file_message)
        if check_type == 0:
            
            return  render_template('index.html',status ="No diagnosis as no file was entered")
        
        elif check_type ==1:
            year = int(request.form['year'])
            month = int(request.form['month'])
            day = int(request.form['day'])
            age = get_age(year,month,day)
            gender = request.form['gender']

            return render_template('index2.html',year = year, month = month,day=day,gender=gender,status = "No diagnosis as no file was entered")
            
        elif check_type ==2:
            return render_template('index4.html',status ="No diagnosis as no file was entered")
     
     if file and allowed_file(file.filename,allowed_extensions): #it checks if the file object exists and if the filename has an allowed extension using the allowed_file function you mentioned earlier. 
             filename = secure_filename(file.filename)
             file.save(os.path.join(upload_folder, filename))

             if check_type == 0:
                  result_sagittal_label,probability_sagittal,result_coronal_label,probability_coronal,result_axial_label,probability_axial,final_label,all_probabilities = MRI.Normalization(upload_folder,filename)

                  AD_probability,CN_probability,MCI_probability = get_label_probability(all_probabilities)

                  global MRI_label
                  MRI_label = final_label
                  global MRI_all_Probabilities
                  MRI_all_Probabilities = all_probabilities
                  global MRI_AD_probability
                  MRI_AD_probability = AD_probability
                  global MRI_CN_probability
                  MRI_CN_probability = CN_probability
                  global MRI_MCI_probability
                  MRI_MCI_probability = MCI_probability

                  global MRI_label_sagittal
                  MRI_label_sagittal = result_sagittal_label
                  global MRI_probability_sagittal
                  MRI_probability_sagittal = probability_sagittal
                  global MRI_label_coronal
                  MRI_label_coronal = result_coronal_label
                  global MRI_probability_coronal
                  MRI_probability_coronal = probability_coronal
                  global MRI_label_axial
                  MRI_label_axial = result_axial_label
                  global MRI_probability_axial
                  MRI_probability_axial= probability_axial

                  sagittal_segment ="Segments/Sagittal " + MRI.get_image_name(filename)+".png"
                  coronal_segment = "Segments/Coronal " + MRI.get_image_name(filename)+".png"
                  axial_segment = "Segments/Axial " + MRI.get_image_name(filename)+".png"

                  global sagittal_image
                  sagittal_image = sagittal_segment
                  global coronal_image
                  coronal_image = coronal_segment
                  global axial_image
                  axial_image = axial_segment

                  return render_template('index.html', result_sagittal = result_sagittal_label,probability_sagittal= probability_sagittal,
                               result_coronal = result_coronal_label,probability_coronal = probability_coronal,result_axial = result_axial_label,
                               probability_axial = probability_axial,final_label = final_label,AD_probability = round(AD_probability,2)*100,
                               CN_probability = round(CN_probability,2)*100,MCI_probability = round(MCI_probability,2)*100,
                               sagittal_segment = sagittal_segment,coronal_segment = coronal_segment,axial_segment = axial_segment) 
             

             elif check_type ==1:
                 
                 year = int(request.form['year'])
                 month = int(request.form['month'])
                 day = int(request.form['day'])

                 age = get_age(year,month,day)

                 gender = request.form['gender']
            
                 gene_predicted_label,gene_all_probabilities = Gene.filtering(upload_folder,filename,age,gender)
                 

                 if gene_predicted_label !="CN":
                     AD_probability,CN_probability,MCI_probability = get_label_probability(gene_all_probabilities)
                     gene_predicted_label = "empty"
                     gene_predicted_label_1,max_prob = Gene.max_of_three_indices(gene_all_probabilities)
                     gene_predicted_label_1 = MRI.get_label(gene_predicted_label_1)
                     AD_MCI_probability = 0

                 elif gene_predicted_label =="CN":
                     AD_MCI_probability = gene_all_probabilities[0] 
                     CN_probability =  gene_all_probabilities[1] 
                     AD_probability = 0
                     MCI_probability = 0
                     gene_predicted_label_1 = "empty"


                 global Gene_predicted_label_1
                 Gene_predicted_label_1 =  gene_predicted_label_1
                 global Gene_pl
                 Gene_pl = gene_predicted_label
                 global Gene_all_probabilities
                 Gene_all_probabilities = gene_all_probabilities
                 global Gene_AD_probability
                 Gene_AD_probability = AD_probability
                 global Gene_CN_probability
                 Gene_CN_probability = CN_probability
                 global Gene_MCI_probability
                 Gene_MCI_probability = MCI_probability
                 global Gene_AD_MCI_probability
                 Gene_AD_MCI_probability = AD_MCI_probability

                 return render_template('index2.html',year = year, month = month,day=day,gender=gender,predicted_label = gene_predicted_label,gene_predicted_label_1 = gene_predicted_label_1,AD_probability = round(AD_probability,2)*100,CN_probability = round(CN_probability,2)*100,MCI_probability = round(MCI_probability,2)*100,AD_MCI_probability = round(AD_MCI_probability,2)*100)
             
             
             elif check_type ==2:
                 #audio_predicted_label,predict_probabilities = Audio.perform_transcription(upload_folder,filename)
                 audio_predicted_label,predict_probabilities = Audio.perform_embeddings(os.path.join(upload_folder,filename))
                 AD_probability,CN_probability,MCI_probability = get_label_probability(predict_probabilities)

                 global Audio_predicted_label
                 Audio_predicted_label = audio_predicted_label
                 global Audio_all_probabilities
                 Audio_all_probabilities = predict_probabilities
                 global Audio_AD_probability
                 Audio_AD_probability = AD_probability
                 global Audio_CN_probability
                 Audio_CN_probability = CN_probability
                 global Audio_MCI_probability
                 Audio_MCI_probability = MCI_probability

                 return render_template('index4.html',predicted_label = audio_predicted_label,AD_probability = round(AD_probability,2)*100,CN_probability = round(CN_probability,2)*100,MCI_probability = round(MCI_probability,2)*100)
                 
     else:
         flash(allowed_types_message)
         if check_type == 0:
            return  render_template('index.html',status = "No diagnosis as format is not allowed")
        
         elif check_type ==1:

            year = int(request.form['year'])
            month = int(request.form['month'])
            day = int(request.form['day'])
            age = get_age(year,month,day)
            gender = request.form['gender']

            return render_template('index2.html',year = year, month = month,day=day,gender=gender,status = "No diagnosis as format is not allowed")
         
         elif check_type ==2:
            return render_template('index4.html',status = "No diagnosis as format is not allowed")
               

def upload_img():
    return upload('file1',MRI_UPLOAD_FOLDER,array_mri_extension,'No image selected for uploading','Allowed image types are nii files',0)

def upload_genetic_data():
    return upload('file',Gene_UPLOAD_FOLDER,array_gene_extension,'No execl file selected for uploading','Allowed file types are csv files',1)

def upload_audio_data():
    return upload('file2',Audio_UPLOAD_FOLDER,array_audio_extension,'No mp3 or wav file selected for uploading','Allowed file types are mp3 or wav files',2)
  

@app.route('/', methods=['GET', 'POST'])
def Run_MRI():
    if request.method == 'POST':
         return upload_img()

    else:
         return render_template('index.html')

@app.route('/Gene', methods=['GET', 'POST'])
def Run_Gene():
    if request.method == 'POST':
        return  upload_genetic_data()
    
    else:
        return render_template('index2.html')
    
@app.route('/Audio', methods=['GET', 'POST'])
def Run_Audio():
    if request.method == 'POST':
        return  upload_audio_data()
    
    else:
        return render_template('index4.html')
    
@app.route('/Results', methods=['GET', 'POST'])
def Run_Results():
        
        hide_gene_flag = False
        final_label,final_array_probability = combine.combine(MRI_all_Probabilities,Gene_all_probabilities,Gene_pl,Audio_all_probabilities)

        if (type(final_array_probability) == int):
            flag_AD_MCI = 0
            AD_probability = 0 
            CN_probability = 0 
            MCI_probability = 0
            AD_MCI_probability = 0

        else:
            if final_label !="CN" and Gene_pl == "CN":
                hide_gene_flag = True

            if (final_label != 0 and len(final_array_probability) !=2):

                AD_probability,CN_probability,MCI_probability = get_label_probability(final_array_probability)
                flag_AD_MCI = 0
                AD_MCI_probability = 0

            elif len(final_array_probability) ==2 and final_label == "CN":
                flag_AD_MCI = 1
                AD_MCI_probability = final_array_probability [0]
                CN_probability = final_array_probability [1]
                AD_probability = 0 
                MCI_probability = 0

        return render_template('index3.html',final_label = final_label,final_AD_probability = round(AD_probability,2)*100,
                               final_CN_probability = round(CN_probability,2)*100,final_MCI_probability = round(MCI_probability,2)*100,

                               gene_predicted_label = Gene_pl,gene_AD_probability = round(Gene_AD_probability,2)*100,
                               gene_CN_probability = round(Gene_CN_probability,2)*100,gene_MCI_probability = round(Gene_MCI_probability,2)*100,

                               audio_label = Audio_predicted_label, audio_AD_probability = round(Audio_AD_probability,2)*100, 
                               audio_CN_probability = round(Audio_CN_probability,2)*100,audio_MCI_probability = round(Audio_MCI_probability,2)*100,

                               mri_label = MRI_label,mri_AD_probability = round(MRI_AD_probability,2)*100,
                               mri_CN_probability = round(MRI_CN_probability,2)*100,mri_MCI_probability = round(MRI_MCI_probability,2)*100,

                               mri_label_sagittal = MRI_label_sagittal, mri_probability_sagittal = MRI_probability_sagittal,
                               mri_label_coronal = MRI_label_coronal, mri_probability_coronal = MRI_probability_coronal,
                               mri_label_axial = MRI_label_axial, mri_probability_axial = MRI_probability_axial,
                               sagittal_image = sagittal_image, coronal_image = coronal_image,axial_image=axial_image,
                               
                               flag_AD_MCI = flag_AD_MCI,final_AD_MCI_probability = round(AD_MCI_probability,2)*100,gene_AD_MCI_probability = round(Gene_AD_MCI_probability,2)*100,
                               Gene_predicted_label_1 = Gene_predicted_label_1,hide_gene_flag = hide_gene_flag)

@app.route('/clear_session')
def clear_session():
    session.clear()

    global MRI_label
    MRI_label = ""
    global MRI_all_Probabilities
    MRI_all_Probabilities = []

    global MRI_label_sagittal
    MRI_label_sagittal = "" 
    global MRI_label_coronal
    MRI_label_coronal = ""
    global MRI_label_axial
    MRI_label_axial = " "

    global Gene_predicted_label_1
    Gene_predicted_label_1 = ""
    global Gene_pl
    Gene_pl = ""
    global Gene_all_probabilities
    Gene_all_probabilities = []

    global Audio_predicted_label
    Audio_predicted_label = ""
    global Audio_all_probabilities
    Audio_all_probabilities = []

    return redirect(url_for('Run_MRI'))

if __name__ == '__main__':
    app.run(debug=True)

    