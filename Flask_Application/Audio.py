import pandas as pd
import numpy as np
from tqdm import tqdm
import os
import joblib
from IPython.display import Audio
import IPython.display
import IPython
import whisper
from torchaudio.utils import download_asset
from collections import Counter
import librosa
import csv
import glob
import soundfile as sf
from flair.models import SequenceTagger
from flair.data import Sentence
from pathlib import Path
import openai
import tiktoken
from openai.embeddings_utils import get_embedding
import joblib


pd.set_option('display.max_rows', None)

def get_label(index):
    
    if index == 0:
        return 'AD'
    if index == 1:
        return 'CN'
    if index == 2:
        return 'MCI'
    

def classify(audio_csv_with_embeddings):

    prev_df = pd.read_csv(audio_csv_with_embeddings)
    new_df = prev_df.drop(["Filename", "Transcription"], axis=1)
    features =  new_df

    xgb_audio = joblib.load("F:/Graduation Project/Flask/Classifiers/XGB_Audios_new.pkl")
    predict_label = xgb_audio.predict(features)
    predict_probabilities = xgb_audio.predict_proba(features)

   
    print("The list of probabilities as predicted by Audio approach:",predict_probabilities)


    return get_label(predict_label),predict_probabilities[0]


def perform_embeddings(audio_csv):

    embedding_model = "text-embedding-ada-002"
    embedding_encoding = "cl100k_base"  # this the encoding for text-embedding-ada-002
    max_tokens = 8000  # the maximum for text-embedding-ada-002 is 8191

    df = pd.read_csv(audio_csv, index_col=0)

    openai.api_key = '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'

    df["embedding"] = df.Transcription.apply(lambda x: get_embedding(x, engine=embedding_model))
    embeddings_df = df["embedding"].apply(lambda x: pd.Series(x, dtype=float)).add_prefix("embedding")

    # Concatenate the embeddings DataFrame with the original DataFrame
    df = pd.concat([df, embeddings_df], axis=1)
    df.drop(columns=["embedding"], inplace=True)  # Drop the original "embedding" column
    df.to_csv(audio_csv)

    predict_label,predict_probabilities = classify(audio_csv)
    return predict_label,predict_probabilities

def get_image_name(filename): 
    return filename.rsplit('.', 1)[0].lower() 

def load_model():
    model = whisper.load_model("base.en")
    print(f"Model is {'multilingual' if model.is_multilingual else 'English-only'} "
          f"and has {sum(np.prod(p.shape) for p in model.parameters()):,} parameters.")
    return model
    
def calculate_ttr(transcription):
    words = transcription.split()
    #print (words)
    num_words = len(words)
    unique_words = len(set(words))
    ttr = unique_words / num_words
    return ttr

def calculate_sdi(transcription):
    words = transcription.split()
    word_counts = Counter(words)
    #print(word_counts)
    num_words = len(words)
    sdi = 1 - sum((count / num_words) ** 2 for count in word_counts.values())
    return sdi

def detect_pauses(audio_file, sr, min_pause_duration=0.5):
    # Load audio file
    audio, sr = librosa.load(audio_file, sr=sr)
    
    # Convert audio to mono if it has multiple channels
    if len(audio.shape) > 1:
        audio = np.mean(audio, axis=1)
    
    # Apply voice activity detection (VAD) or other methods to segment speech
    
    # Example using librosa VAD
    speech_segments = librosa.effects.split(audio, top_db=20)
    
    # Calculate pause durations between speech segments
    #sr = bundle.sample_rate
    pause_durations = []
    pauses = []
    prev_end = 0.0
    for start, end in speech_segments:
        pause_duration = start - prev_end
        if pause_duration >= min_pause_duration:
            pauses.append(pause_duration)
        prev_end = end
    for pause in pauses:
        pause_duration = pause / sr
        pause_durations.append(pause_duration)
        
    total_duration = len(audio_file) / sr
    pause_rate = sum(pause_durations) / total_duration
    return pause_rate 

def calculate_syntactic_complexity(transcription):
    sentences = transcription.split('.')  # Split text into sentences assuming period (.) as the sentence delimiter
    num_sentences = len(sentences)
    
    total_clauses = 0
    num_words = 0
    for sentence in sentences:
        words = sentence.split()
        num_words += len(words)
        
        tagger = SequenceTagger.load('pos')
        line = Sentence(sentence)
        tagger.predict(line)
        pos_tags = [(token.text, token.labels[0].value) for token in line]

        num_clauses = 0
        for i in range(len(pos_tags)-1):
            current_tag = pos_tags[i][1]
            next_tag = pos_tags[i+1][1]
            if current_tag.startswith('V') and next_tag not in ['.', ':', 'IN']:
                num_clauses += 1
        total_clauses += num_clauses
    
    average_sentence_length = num_words / num_sentences
    average_clauses_per_sentence = total_clauses / num_sentences

    #print(num_words)
    #print(num_sentences)
    #print(total_clauses)

    return average_sentence_length, average_clauses_per_sentence

def perform_transcription(upload_folder,filename):

    audio_file = os.path.join(upload_folder,filename)
    audio_csv_file_directory= "F:/Graduation Project/Flask/Audio_csv/"
    audio_csv_file_name = f"output_{get_image_name(filename)}.csv"
    output_file = os.path.join(audio_csv_file_directory,audio_csv_file_name)


    with open(output_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Filename", "Transcription", "Speech Rate", "Pause Rate", "Lexical Diversity(SDI Score)", "Syntactic Complexity(Avg Clauses per)"])

        # Display Audio
        audio_display = Audio(audio_file)
        IPython.display.display(audio_display)

        # Perform Transcription
        model = load_model()
        transcription_dict = model.transcribe(audio_file)
        transcription_text = transcription_dict['text']
        print(transcription_text)

        #perform 4 features of alzheimers
        #get Segements and Number of words
        segments = transcription_dict["segments"]
        num_words = len(transcription_text.split())
        #print(f"Transcription for {m}: {transcription_text}\n")
 
        #Calculate speech rate
        audio_info = sf.info(audio_file)
        duration = audio_info.duration
        sample_rate = audio_info.samplerate
        frame_duration = 0.01
        num_frames = int(duration * sample_rate / frame_duration)
 
        #The formula calculates the average number of words spoken per second 
        #based on the number of words in the transcription and the duration of the audio file.
        speech_rate = num_words / (num_frames / sample_rate)
        print("Speech Rate (WPS):", speech_rate)

        #Lexical diversity using TTR 
        ttr_score = calculate_ttr(transcription_text)
        print("TTR Score:", ttr_score)
    
        #Lexical diversity using sdi 
        sdi_score = calculate_sdi(transcription_text)
        print("SDI Score:", sdi_score)

        #Pause Rate 
        pauses = detect_pauses(audio_file,sr=sample_rate)
        print("Pause:", pauses)
    
        #Syntactic Complexity:
        avg_sentence_length, avg_clauses_per_sentence = calculate_syntactic_complexity(transcription_text)
        print("Average Sentence Length:", avg_sentence_length)
        print("Average Clauses per Sentence:", avg_clauses_per_sentence)
        
        # Write the filename, transcription, and features to the CSV file
        csv_writer.writerow([os.path.basename(audio_file), transcription_text,speech_rate, pauses, sdi_score, avg_clauses_per_sentence])
    
    predict_label,predict_probabilities = perform_embeddings(output_file)
    return predict_label,predict_probabilities


        
   

    
   
    
   
    
    
  
    
    







