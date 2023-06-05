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


#===============================================================
# DEFINE PARAMETERS
#===============================================================

# Relative path to data folders
data_path = './Data'

# Define dictionaries to store dataframes
clinical_dfs = {}
mutation_dfs = {}

# File names: 
clinical_file_name = 'data_clinical_patient.txt'
#mutation_file_name = 


# Define regular expression to get study name from path
study_name_re = r'(?<=Data\/).*'


#===============================================================
# DEFINE FUNCTIONS
#===============================================================

# Create a list of study data included in Data folder:
def get_data_dirs(directory):
    data_dirs = []
    
    for entry in os.scandir(directory):
        if entry.is_dir():
            data_dirs.append(entry.path)
            
    return data_dirs





# Read clinical data files into dictionary of dataframes: 
# For each included data folder: 
for path in data_included:
    # Read clinical data files:
    clinical_file_path = os.path.join(path, clinical_file_name)
    if os.path.isfile(clinical_file_path):
        clinical_df = pd.read_csv(clinical_file_path, header=0, delimiter='\t')
        clinical_dfs[path] = clinical_df
    

# Define function that adds column containing study name to each df
def add_dataframe_name_column(dataframes):
    for name in dataframes:
        dataframe = dataframes[name]
        dataframe['study_name'] = re.search(r'(?<=Data\/).*', name).group()

# Run on each dictionary of dfs:
add_dataframe_name_column(clinical_dfs)



# Define function that concatinates dataframes in dict: 
def concatinate_dfs(df_dict):
    dfs = []
    for df in df_dict.values():
        dfs.append(df)
        concatinated_df = pd.concat(dfs, ignore_index = True)
    
    return concatinated_df

# Run on each dictionary of dfs:
test_concatinated = concatinate_dfs(clinical_dfs)


#===============================================================
# RUN FUNCTIONS ON DATA
#===============================================================

# Get path to directories included in data folder
data_included = get_data_dirs(data_path)


    






