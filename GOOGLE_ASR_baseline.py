# -*- coding: utf-8 -*-
"""
Created on Mon Jan  7 21:50:03 2019

@author: HuangChengChou
"""


import glob
import os
from pydub import AudioSegment
AudioSegment.converter = r'/usr/bin/ffmpeg'
import io
# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
#from google.cloud import storage
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]='/home/jack/Desktop/GoogleASRBaseline-d53db77c0b7e.json'



    
def Google_ASR(Path,long=0,gcs_uri=''):
    Fs = 16000
#    Path = 'E:/NNIME Audio Platform/Sentence_modified/angry/01/angry_01_A_2.wav'
     
    # Instantiates a client
    client = speech.SpeechClient()
    
    if (long==0):
        # Loads the audio into memory
        with io.open(Path, 'rb') as audio_file:
            content = audio_file.read()
            audio = types.RecognitionAudio(content=content)
        
        audio = types.RecognitionAudio(content=content)
        config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=Fs,
            language_code='cmn-Hant-TW')
        
        # Detects speech in the audio file
        response = client.recognize(config, audio)
    else:        
    
        audio = types.RecognitionAudio(uri=gcs_uri)
        config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code='cmn-Hant-TW')
        
        operation = client.long_running_recognize(config, audio)
        
        print('Waiting for operation to complete...')
        response = operation.result(timeout=90)
#    try:
#        response = client.recognize(config, audio)
#    except:
#        audio = types.RecognitionAudio(content=content)
#        response = client.long_running_recognize(config, audio)

    
    response_list = response.results
    transcripts="None"
    if len(response_list) !=0:
        for result in response.results:
            transcripts = result.alternatives[0].transcript
#    for result in response.results:
#        print('Transcript: {}'.format(result.alternatives[0].transcript))
    
    
    return transcripts

#Path = 'F:/Cowork/ITRI_BIIC/Meeting_Database/181119_home_fir/Out_1/chunk-03.wav'
#print(Google_ASR(Path))




# =============================================================================
    
# Short Sentences
    
# =============================================================================
Path = '/home/jack/formosa_add/*.wav'
outpath= '/home/jack/formosa_decode/'
Files_list = glob.glob(Path)


f=open(outpath+"formosa_test.txt","w")
f_exclude=open(outpath+"formosa_exclude.txt","w")
for i,item_txt in enumerate(Files_list):

    Name = item_txt.split("/")[-1].split(".")[0]
    try:
        transcripts = Google_ASR(item_txt)
        Write = Name + "\t" + transcripts + "\n"
        f.write(Write)
    except:
        gcs_uri='gs://formosatest/{0}'.format(Name)
        transcripts = Google_ASR(item_txt,gcs_uri=gcs_uri)
        f_exclude.write(str(i)+"\t"+Name+"\n")        
    print("Processing utterance "+Name+" number "+ str(i))
          
 
    
f.close()

# =============================================================================
    
# Long Sentences
    
# =============================================================================



















            