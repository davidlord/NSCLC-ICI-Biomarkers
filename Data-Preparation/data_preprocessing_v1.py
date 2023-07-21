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

mutations_file_path = "mutations.txt"

# Relative path to data folders directory
data_path = './Data'

# File names from cBioPortal: 
clinical_file_name = 'data_clinical_patient.txt'
sample_file_name = 'data_clinical_sample.txt'
mutation_file_name = 'data_mutations.txt'



#===============================================================
# READ MUTATIONS REFERENCE FILE
#===============================================================

# Read contents of mutations text file
with open(mutations_file_path, "r") as file:
    file_content = file.read()

# Split the content by commas and create a list of mutations of interest
mutations_of_interest_list = file_content.split(",")

# removw leading/trailing whitespaces
mutations_of_interest_list = [item.strip() for item in mutations_of_interest_list]

# Print mutations of interest
print("Mutations of interest specified in file: ")
for mut in mutations_of_interest_list:
    print(mut)



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
            df = pd.read_csv(file_path, header=0, delimiter='\t', low_memory=False)
            data_dict[path] = df
            print("Successfully read: " + file_path)


# Add column containing study name to each df
def add_dataframe_name_column(dataframes_dict):
    for df_name in dataframes_dict:
        df = dataframes_dict[df_name]
        df['study_name'] = re.search(r'(?<=Data\/).*', df_name).group()


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

# GET PATH to directories included in data folder
data_included = get_data_dirs(data_path)


# REMOVE COMMENTED LINES from mutations data files
    # Clinical data: 
remove_commented_lines(data_included, clinical_file_name)
    # Sample data: 
remove_commented_lines(data_included, sample_file_name)
    # Mutational data:
remove_commented_lines(data_included, mutation_file_name)


# DEFINE DICTIONARIES to store dataframes
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
    

# ADD STUDY NAME as column to dataframes in dictionaries
    # Clinical data: 
add_dataframe_name_column(clinical_dfs)
    # Sample data: 
add_dataframe_name_column(sample_dfs)
    # Mutational data: 
add_dataframe_name_column(mutation_dfs)


# CONCATINATE DATAFRAMES in dicts into single dataframe
    # Clinical data:
all_clinical_data = concatinate_dfs(clinical_dfs)
    # Sample data: 
all_sample_data = concatinate_dfs(sample_dfs)
    # Mutational data:
all_mutations_data = concatinate_dfs(mutation_dfs)


# FILTER mutations not included in mutations of interest list
mutations_filtered = all_mutations_data[all_mutations_data['Hugo_Symbol'].isin(mutations_of_interest_list)]


#####    DEV     #######

# Create simplified dataframe of 10 rows
temp_df = mutations_filtered.head(10)

# FILTER to KEEP only relevant columns
temp_df = temp_df[['Tumor_Sample_Barcode', 'Hugo_Symbol', 'Variant_Type', 'Consequence']]




#####    DEV     #######

# AIM
#--------

# Now time for some data engineering :)

# We want a dataset in which each row represents a patient and mutations of interests are columns. 
# However, mutations are currently manifested as rows in the mutations df. 

# The sample dataset is needed to link information together between the clinical df 
# and mutational df, see data relations information below for details. 

# IDEA: 
    
    # Define a list of genes of interest, place in other file.
    
    # Go through mutations df, keep only rows in which Hugo_Symbol matches a gene in list
        # Store in temp_df
    
    # Join patient and sample tables to joined_df
    
    # Add mutation names in mutations_of_interest_list as columns to joined_df
    
    # For each row in joined_df
        # if joined_df[tumor_sample_barcode] = temp_df[tumor_sample_barcode]
            # tempvar = temp_df[Hugo_Symbol]
            # joined_df[tempvar] = TRUE
    



# DATA RELATIONS BETWEEN TABLES:
#-----------------------------------------
# JOIN DATAFRAMES to single dataset
# CLINICAL DATA: PK = "PATIENT_ID"
# SAMPLE DATA: PK = "SAMPLE_ID", FK on Clinical = "PATIENT_ID"
# MUTATIONS DATA: FK on Sample = "Tumor_Sample_Barcode"


# COLUMNS OF INTEREST: 
#-----------------------
# CLINICAL DATA: 
# SAMPLE DATA: 
#MUTATIONS DATA: "Hugo_Symbol", "Consequence", "Variant_Type", and "Tumor_Sample_Barcode"



# WRITE FILES: Concatinated dataframes



#===============================================================
# DEBUG
#===============================================================










