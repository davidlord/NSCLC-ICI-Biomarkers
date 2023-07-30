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
import matplotlib.pyplot as plt
import seaborn as sns
import openpyxl


os.getcwd()
os.chdir('/Users/davidlord/Documents/GitHub/NSCLC-ICI-Biomarkers/Data-Preparation')



#===============================================================
# DEFINE PARAMETERS
#===============================================================
# Move some of these to config file?

mutations_file_path = "mutations.txt"
column_names_config_file = "column_names_config.txt"


# Relative path to data folders directory
data_path = './Data'

# File names from cBioPortal: 
clinical_file_name = 'data_clinical_patient.txt'
sample_file_name = 'data_clinical_sample.txt'
mutation_file_name = 'data_mutations.txt'


#===============================================================
# DEFINE FUNCTIONS
#===============================================================

# RUNS FOR BOTH INSTANCES
#-------------------------

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


# Check if column_names.txt file exists or not
def check_column_names_file():
    file_name = 'column_names.txt'
    if os.path.isfile(file_name):
        return True
    else:
        return False

# READ lines from text file
def read_lines_from_file(filename):
    lines = []
    with open(filename, 'r') as file:
        for line in file:
            lines.append(line.strip())
    return lines


# SEARCH for FILENAME
def search_file_in_current_directory(filename):
    file_status = False
    current_directory = os.getcwd()

    for root, _, files in os.walk(current_directory):
        for file in files:
            if file == filename:
                return os.path.join(root, file)
                file_status = True

    return file_status
    
    
# WRITE text file 
def write_txt_file(text_body, output_file_path):
    try:
        with open(output_file_path, 'w') as text_file:
            text_file.write(text_body)
    except Exception as e:
        print(f"Error occurred while writing to the text file: {e}")

# WAIT for confirmation
def wait_for_confirmation():
    while True:
        user_input = input("Please enter 'y' or 'Y' to continue: ")
        if user_input.lower() == 'y':
            break
        else:
            print("Invalid input. Please try again.")

    print("User confirmed. Proceeding with further code execution...")
    # Put your code here that you want to execute after the user confirms with 'y' or 'Y'


# PARSE column_name_harmonization.txt
def parse_column_name_harmonization(file_path):
    parsed_dict = {}
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line.startswith('#'):
                key, values = line.split('=', 1)
                key = key.strip()
                values = [value.strip() for value in values.split(',')]
                parsed_dict[key] = values
    return parsed_dict

# CHANGE column names based on dictionary of lists
def change_column_names(df_partitions_dict, parsed_dict):
    for df_key, df in df_partitions_dict.items():
        for column_name in df.columns:
            for key, value_list in parsed_dict.items():
                if column_name in value_list:
                    new_column_name = key
                    df.rename(columns={column_name: new_column_name}, inplace=True)


# WRITE column entries in harmonized column names df
def write_categorical_columns_to_file(df, output_file):
    # Select only the categorical columns in the DataFrame
    categorical_columns = df.select_dtypes(include='category').columns

    # Open the output file in write mode
    with open(output_file, 'w') as file:
        # Loop through each categorical column
        for column_name in categorical_columns:
            file.write(f"{column_name}: ")
            unique_entries = df[column_name].unique()
            entries_str = ", ".join(map(str, unique_entries))
            file.write(entries_str)
            file.write("\n")



#===============================================================
# EXECUTE FUNCTIONS
#===============================================================


# DATA PREPARATION
#====================================================================

# REAT MUTATIONS of interest text file
mutations_of_interest_list = read_lines_from_file("mutations.txt")
print("Mutations of interest specified in file: ")
for mut in mutations_of_interest_list:
    print(mut)

# GET PATH to directories included in data folder
data_included = get_data_dirs(data_path)


# REMOVE COMMENTED LINES from data files
    # Clinical data: 
remove_commented_lines(data_included, clinical_file_name)
    # Sample data: 
remove_commented_lines(data_included, sample_file_name)
    # Mutations data:
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
    # Mutations data: 
read_data(data_included, mutation_file_name, mutation_dfs)

# ADD STUDY NAME as column to dataframes in dictionaries
    # Clinical data: 
add_dataframe_name_column(clinical_dfs)
    # Sample data: 
add_dataframe_name_column(sample_dfs)
    # Mutations data:
add_dataframe_name_column(mutation_dfs)

# CONCATINATE DATAFRAMES in dicts into single dataframe
    # Clinical data:
all_clinical_data = concatinate_dfs(clinical_dfs)
    # Sample data: 
all_sample_data = concatinate_dfs(sample_dfs)
    # Mutational data:
all_mutations_data = concatinate_dfs(mutation_dfs)

# JOIN clinical- and sample dataframes to single
patient_sample_data = pd.merge(all_clinical_data, all_sample_data, on='PATIENT_ID', how='left')


# GET USER INPUT TO DEFINE DATA PROCESSING
#====================================================================
### DEV ###

# STEP 1: Get input for relevant columns
#-----------------------------------------------

# Visualize NA values in joined df
#-----------------------------------------------

# Count NA entries
na_counts = patient_sample_data.isna().sum()

# Create a bar plot
plt.figure(figsize=(10, 6))
sns.barplot(x=na_counts.index, y=na_counts.values)
plt.xticks(rotation=90)
plt.title("NA Entries in Dataset")
plt.xlabel("Columns")
plt.ylabel("Number of NA Entries")
plt.tight_layout()  # To avoid labels being cut off in saved image
plt.savefig("na_bar_plot.png")
plt.close()  # Close the figure to free up memory

# Create a heatmap for NA values
plt.figure(figsize=(8, 6))
sns.heatmap(df.isna(), cmap="viridis", cbar=False, yticklabels=False)
plt.title("NA Values Heatmap")
plt.tight_layout()  # To avoid labels being cut off in saved image
plt.savefig("na_heatmap.png")
plt.close()  # Close the figure to free up memory

# WRITE COLUMN names text files
# DEFINE column names string
column_names_string = ""
column_names = patient_sample_data.columns.tolist()
for column_name in column_names:
    column_names_string = column_names_string + column_name + '\n'


# WRITE column names text file and one for columns of interest
write_txt_file(column_names_string, "column_names.txt")
print("File written: column_names.txt")

write_txt_file(column_names_string, "columns_of_interest.txt")

# PRINT instructions
print('---------------------------------')
print("File written: columns_of_interest.txt")
print('Please open the "columns_of_interest.txt" file, remove remove columns that are not of interest, and save file')
print('See the "na_bar_plot.png" and the "na_heatmap.png" files in the current directory to view how many entries of each column is missing data')
print("Please do this before proceeding to the next step.")
print('---------------------------------')


# WAIT for user to provide input
wait_for_confirmation()


# STEP 2: Get input for column harmonization
#----------------------------------------------

# READ columns of interest txt file
keep_cols = read_lines_from_file("columns_of_interest.txt")

# FILTER: Keep only columns of interest
patient_sample_data_filtered = patient_sample_data.filter(keep_cols)

# Visualize NA values in filtered df
#-----------------------------------------------

# Create a bar plot
plt.figure(figsize=(10, 6))
sns.barplot(x=na_counts.index, y=na_counts.values)
plt.xticks(rotation=90)
plt.title("NA Entries in Dataset")
plt.xlabel("Columns")
plt.ylabel("Number of NA Entries")
plt.tight_layout()  # To avoid labels being cut off in saved image
plt.savefig("filtered_na_bar_plot.png")
plt.close()  # Close the figure to free up memory

# Create a heatmap for NA values
plt.figure(figsize=(8, 6))
sns.heatmap(df.isna(), cmap="viridis", cbar=False, yticklabels=False)
plt.title("NA Values Heatmap")
plt.tight_layout()  # To avoid labels being cut off in saved image
plt.savefig("filtered_na_heatmap.png")
plt.close()  # Close the figure to free up memory

# WRITE column names txt file
#--------------------------------

# DEFINE column names string
column_names_string = ""
column_names = patient_sample_data_filtered.columns.tolist()
for column_name in column_names:
    column_names_string = column_names_string + column_name + '\n'

# WRITE column names text file and one for column name harmonization
write_txt_file(column_names_string, "filtered_column_names.txt")
print("File written: filtered_column_names.txt")

# DEFINE column names config string
column_names_config_string = "# Please define the columns that represent the same information in this text file following the example rows below, excluding hashes\n"
column_names_config_string = column_names_config_string + "# TMB = TMB, NONSYNONYMOUS_MUTATION_BURDEN, TMB_NONSYNONYMOUS, TOTAL_EXONIC_MUTATION_BURDEN\n"
column_names_config_string = column_names_config_string + "# AGE = AGE, AGE_CURRENT, AGE_AT_SURGERY, AGE_YRS, AGE_AT_SEQ_REPORTED_YEARS"
# WRITE column name harmonization txt file
write_txt_file(column_names_config_string, "column_name_harmonization.txt")

# PRINT instructions
print('---------------------------------')
print('A list of the remaining columns can be found in the "filtered_column_names.txt" file')
print('Please guide the column name harmonization process by filling in the "column_name_harmonization.txt file"')
print('See the "filtered_na_bar_plot.png" and the "filtered_na_heatmap.png" files in the current directory to view how many entries of each column is missing data')
print("Please do this before proceeding to the next step.")
print('---------------------------------')

# APPLY changes
#-------------------------------

# WAIT for user to provide input
wait_for_confirmation()


# HARMONIZE column names
df_partitions_dict = {}
grouped = patient_sample_data_filtered.groupby('study_name')

# Iterate over each group and store dictionary
for study_name, group in grouped:
    df_partitions_dict[study_name] = group.copy()  # Using .copy() to ensure a new DataFrame for each partition


# Parse column names harmonization txt file
# Store entries in dict:
parsed_dict = parse_column_name_harmonization("column_name_harmonization.txt")

# CHANGE column names
change_column_names(df_partitions_dict, parsed_dict)

# CONCATINATE to single df again
patient_sample_df_colnames_harmonized = pd.concat(df_partitions_dict.values(), ignore_index=True)




# STEP 3: Get input for categories harmonization
#----------------------------------------------

# WRITE categorical entries for each column to a text file:
write_categorical_columns_to_file(patient_sample_df_colnames_harmonized, "categories_harmonization.txt")









#===============================================================
# EXECUTE FUNCTIONS: WRITE DATASET MODULE
#===============================================================




##### DEV #########

# Keep only relevant columns in all_mutations data


# Filter to keep only MUTATIONS of interest in all_mutations data



# Create a new df ("sample_temp_df") holdinhg a subset of columns from sample df. 

# For each gene of interest in genes_of_interest_list: 
    # Add gene_name as column to sample_temp_df, set all values to empty string or something



# For each row in sample_temp_df: 
    # If all_mutations_df[SAMPLE_ID] == sample_temp_df[SAMPLE_ID]
        # tempvar = all_mutations_df[Hugo_Symbol]
        # sample_temp_df[tempvar] = all_mutations_df[Consequence
        
        
# Then somehow relate sample_temp_df to clinical data...

#------------------

# KEEP only RELEVANT columns in mutations data:
all_mutations_data = all_mutations_data[['Tumor_Sample_Barcode', 'Hugo_Symbol', 'Consequence', 'Mutation_Status']]

# FILTER: KEEP only genes defined in GENES OF INTEREST LIST
mutations_data = all_mutations_data[all_mutations_data['Hugo_Symbol'].isin(mutations_of_interest_list)]










### DEV #####
# HOW TO DEAL WITH MULTIPLE SAMPLES / PATIENT???

# MERGE samples and patients table to single: 
    sample_patient_df = pd.merge(all_sample_data, all_clinical_data, on='PATIENT_ID', how='inner')
    
    
    # Investigate duplicates
    duplicate_rows = sample_patient_df[sample_patient_df.duplicated(subset='PATIENT_ID', keep=False)]
    dup_sample_patients = sample_patient_df.duplicated(subset=['PATIENT_ID'])
    
    duplicates_specific_cols = df.duplicated(subset=['column1', 'column2'])
    


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










