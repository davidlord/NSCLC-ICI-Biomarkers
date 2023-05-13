#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  1 19:01:44 2023

@author: davidlord
"""
# Import packages:
import os
import re
import pandas as pd
import glob


os.getcwd()
os.chdir('/Users/davidlord/Documents/GitHub/NSCLC-ICI-Biomarkers/Data-Preparation')

data_path = './Data'
# Create a list of study data included in Data folder:
def get_data_dirs(directory):
    data_dirs = []
    
    for entry in os.scandir(directory):
        if entry.is_dir():
            data_dirs.append(entry.path)
            
    return data_dirs

data_included = get_data_dirs(data_path)


#===============================================================
# DEFINE SOME STUFF FOR THE READ DATA FUNCTION BELOW
#===============================================================

# Define dictionaries to store dataframes
clinical_dfs = {}
mutation_dfs = {}

# File names: 
clinical_file_name = 'data_clinical_patient.txt'
#mutation_file_name = 

# Define study names list:
study_names = []

# Define regular expression to get study name from path
study_name_re = r'(?<=Data\/).*'


# For each included project: 
for data_path in data_included:
    # Get study name:
    study_names.append(re.search(study_name_re, data_path).group())
        
   # Read clinical data files:
    clinical_file_path = os.path.join(data_path, clinical_file_name)
    #print(clinical_file_path)
    if os.path.isfile(clinical_file_path):
        clinical_df = pd.read_csv(clinical_file_path, header=0, delimiter='\t')
        clinical_dfs[data_path] = clinical_df
        
        
        
        
        study_name+"clinical_data" = pd.read_csv(data_path+'data_clinical_patient.txt', header=0, delimiter='\t')



        
    
study_name = pd.read_csv('Data/luad_mskcc_2015/data_clinical_patient.txt', header=0, delimiter='\t')




study_name = re.search(study_name_re, './Data/nsclc_pd1_msk_2018').group()

clinical_data_files_list = []


clinical_data_1 = pd.read_csv('Data/luad_mskcc_2015/data_clinical_patient.txt', header=0, delimiter='\t')
e
clinical_data_2 = pd.read_csv('Data/luad_mskcc_2020/data_clinical_patient.txt', header=0, delimiter='\t')
e






