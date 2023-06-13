from flask import Flask, render_template, request, session, redirect, flash, url_for
from werkzeug.utils import secure_filename
import os
from tqdm import tqdm
import MRI
import Gene
import combine
import datetime

app = Flask(__name__)
#UPLOAD_FOLDER = '/home/farah/Documents/softwareApp/HistoryUploads'
MRI_UPLOAD_FOLDER = 'F:/Graduation Project/Flask/MRI_Uploads/'
Gene_UPLOAD_FOLDER = 'F:/Graduation Project/Flask/Gene_Uploads/'
app.secret_key = "MRI-flask" #for browser cookies for security.
ALLOWED_EXTENSIONS_MRI = set(['nii'])
ALLOWED_EXTENSIONS_GENE = set(['csv'])

MRI_Probabilities = []
Gene_Probabilities_Label=0
Gene_Probabilities_max_result_1 = 0
Gene_predicted_label = ""
Gene_filename = ""

MRI_label=""
MRI_combined_probability=0
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
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


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
        

def upload(file_name,upload_folder,allowed_extensions,empty_file_message,successful_upload_message,allowed_types_message,check_type):
     
     if file_name not in request.files: #dict. and check with key file1 to ensure that a file was indeed submitted in the request.
        flash('No file part')

        if check_type == 0:
            return  redirect(url_for('Run_MRI'))
        
        elif check_type ==1:
            return redirect(url_for('Run_Gene'))
        
         
     file = request.files[file_name] #retrieve file with key file1
        
     if file.filename == '':
        flash(empty_file_message)
        if check_type == 0:
            return  redirect(url_for('Run_MRI'))
        
        elif check_type ==1:
            return redirect(url_for('Run_Gene'))
     
     if file and allowed_file(file.filename,allowed_extensions): #it checks if the file object exists and if the filename has an allowed extension using the allowed_file function you mentioned earlier. 
             filename = secure_filename(file.filename)
             file.save(os.path.join(upload_folder, filename))
             flash(successful_upload_message)

             if check_type == 0:
                  result_sagittal_label,probability_sagittal,result_coronal_label,probability_coronal,result_axial_label,probability_axial,final_label, combined_probability,all_probabilities = MRI.Normalization(upload_folder,filename)
                  global MRI_Probabilities 
                  MRI_Probabilities = all_probabilities

                  global MRI_label
                  MRI_label = final_label
                  global MRI_combined_probability
                  MRI_combined_probability = combined_probability*100

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
                               probability_axial = probability_axial,final_label = final_label, combined_models_probability =  combined_probability*100,
                               sagittal_segment = sagittal_segment,coronal_segment = coronal_segment,axial_segment = axial_segment) 
             

             elif check_type ==1:
                 
                 year = int(request.form['year'])
                 month = int(request.form['month'])
                 day = int(request.form['day'])

                 age = get_age(year,month,day)

                 gender = request.form['gender']
            
                 predicted_label,probability_shown,probability_needed_combine = Gene.filtering(Gene_UPLOAD_FOLDER,filename,age,gender)

                 global Gene_Probabilities_Label
                 Gene_Probabilities_Label = probability_shown
                 global Gene_Probabilities_max_result_1
                 Gene_Probabilities_max_result_1 = probability_needed_combine
                 global Gene_predicted_label
                 Gene_predicted_label = predicted_label
                 global Gene_filename
                 Gene_filename = filename

                 return render_template('index2.html',year = year, month = month,day=day,gender=gender, predicted_label = predicted_label,probability = probability_shown*100)
                 
     else:
         flash(allowed_types_message)
         if check_type == 0:
            return  redirect(url_for('Run_MRI'))
        
         elif check_type ==1:

            year = int(request.form['year'])
            month = int(request.form['month'])
            day = int(request.form['day'])
            age = get_age(year,month,day)
            gender = request.form['gender']

            return render_template('index2.html',year = year, month = month,day=day,gender=gender)
               

def upload_img():
    return upload('file1',MRI_UPLOAD_FOLDER,ALLOWED_EXTENSIONS_MRI,'No image selected for uploading','Image successfully uploaded','Allowed image types are nii files',0)

def upload_genetic_data():
    return upload('file',Gene_UPLOAD_FOLDER,ALLOWED_EXTENSIONS_GENE,'No execl file selected for uploading','Excel file successfully uploaded','Allowed file types are csv files',1)
  

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
    
@app.route('/Results', methods=['GET', 'POST'])
def Run_Results():
        
        final_label,final_label_probability = combine.combine(MRI_Probabilities,Gene_Probabilities_Label,Gene_Probabilities_max_result_1,Gene_predicted_label,Gene_UPLOAD_FOLDER,Gene_filename)
        return render_template('index3.html',final_label = final_label,final_label_probability = round(final_label_probability,2)*100,gene_predicted_label = Gene_predicted_label,gene_probability = Gene_Probabilities_Label*100,
                               mri_label = MRI_label,mri_probability = MRI_combined_probability, mri_label_sagittal = MRI_label_sagittal, mri_probability_sagittal = MRI_probability_sagittal,
                               mri_label_coronal = MRI_label_coronal, mri_probability_coronal = MRI_probability_coronal,mri_label_axial = MRI_label_axial, mri_probability_axial = MRI_probability_axial,
                               sagittal_image = sagittal_image, coronal_image = coronal_image,axial_image=axial_image)

if __name__ == '__main__':
    app.run(debug=True)

    