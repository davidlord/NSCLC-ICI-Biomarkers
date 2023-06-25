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
# DEV: Move some of these to config file

# Relative path to data folders
data_path = './Data'

# File names: 
clinical_file_name = 'data_clinical_patient.txt'
sample_file_name = 'data_clinical_sample.txt'
mutation_file_name = 'data_mutations.txt'



#===============================================================
# DEFINE FUNCTIONS
#===============================================================
                
# Create a list of study data included in Data folder
def get_data_dirs(directory):
    data_dirs = []
    
    for entry in os.scandir(directory):
        if entry.is_dir():
            data_dirs.append(entry.path)
    print("Data directories included:")
    for i in data_dirs:
        print(i)
            
    return data_dirs


# Remove commented lines (start with '#') from data files
def remove_commented_lines(path_list, name):
    for path in path_list:
        # Define file paths
        file_path = os.path.join(path, name)
        # read files
        with open(file_path, 'r') as file:
            lines = file.readlines()
        # Write file, keep only lines that do not start with '#'
        keep_lines = [line for line in lines if not line.startswith('#')]
        
        with open(file_path, 'w') as file:
            file.writelines(keep_lines)
        print("Successfully removed commented lines from: " + file_path)



# Read file that matches name in path into dictionary of dataframes
# Loop over directories included
def read_data(path_list, name, data_dict):
    for path in path_list:
    # Read data files:
        file_path = os.path.join(path, name)
        if os.path.isfile(file_path):
            df = pd.read_csv(file_path, header=0, delimiter='\t')
            data_dict[path] = df
            print("Successfully read: " + file_path)



# Add column containing study name to each df
def add_dataframe_name_column(dataframes_dict):
    for df_name in dataframes_dict:
        df = dataframes_dict[df_name]
        df['study_name'] = re.search(r'(?<=Data\/).*', df_name).group()


def remove_nonsense_rows(dataframes_dict):
    for df_name in dataframes_dict:
        df = dataframes_dict[df_name]
        df = df.iloc[4:]
        dataframes_dict[df_name] = df
    


# Concatinate dataframes in dict into single dataframe: 
def concatinate_dfs(df_dict):
    dfs = []
    for df in df_dict.values():
        dfs.append(df)
        concatinated_df = pd.concat(dfs, ignore_index = True)
    
    return concatinated_df




#===============================================================
# RUN FUNCTIONS ON DATA
#===============================================================

# Get path to directories included in data folder
data_included = get_data_dirs(data_path)

# Remove commented lines from mutations data files
remove_commented_lines(data_included, mutation_file_name)

# Define dictionaries to store dataframes
clinical_dfs = {}
sample_dfs = {}
mutation_dfs = {}


# READ DATA tables into dictionary of dataframes
    # Clinical data: 
read_data(data_included, clinical_file_name, clinical_dfs)
    # Sample data:
read_data(data_included, sample_file_name, sample_dfs)
    # Mutational data: 
read_data(data_included, mutation_file_name, mutation_dfs)
    

# FILTER nonsense rows from dataframes
    # Clinical data:
remove_nonsense_rows(clinical_dfs)

# ADD STUDY NAME as column do dataframes in dictionaries
    # Clinical data: 
add_dataframe_name_column(clinical_dfs)
    # Mutational data: 

# CONCATINATE DATAFRAMES in dicts into single dataframe
    # Clinical data:
all_clinical_data = concatinate_dfs(clinical_dfs)






#===============================================================
# UNDER DEVELOPMENT
#===============================================================

# Read mutations table into df
mutations_df = pd.read_csv('Data/nsclc_mskcc_2018/data_mutations_mskcc.txt', header=0, delimiter='\t')

# read sample tables 




#===============================================================
# DEBUG
#===============================================================


# Usage example:
file_path = './Data/luad_mskimpact_2021/data_mutations.txt'
remove_commented_lines(file_path)


# Unable to read the mutations file from luad_mskimpact_2021 for some reason
file_path = "./Data/luad_mskimpact_2021/data_mutations.txt"
test_df = pd.read_csv(file_path, header=0, delimiter='\t')







