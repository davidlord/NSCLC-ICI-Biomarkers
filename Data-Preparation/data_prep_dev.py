#!/usr/bin/env python3
print("helo")

# Import packages:
import os
import re
import pandas as pd
import glob
import matplotlib.pyplot as plt

### TEMP path
C:\Users\kxvz994\Documents\NSCLC-ICI-Biomarkers\Data-Preparation



# DEFINE PARAMETERS

### Move some of these to config file?
mutations_file = "mutations.txt"
column_names_config_file = "column_names_config.txt"


# Relative path to data folders directory
data_path = './Data'

# File names from cBioPortal: 
patient_file_name = 'data_clinical_patient.txt'
sample_file_name = 'data_clinical_sample.txt'
mutation_file_name = 'data_mutations.txt'


#===============================================================
# DEFINE FUNCTIONS
#===============================================================


# DATA HANDLING & PROCESSING
#---------------------------------------------------------------
# READ lines from text file
def read_lines_from_file(filename):
    lines = []
    with open(filename, 'r') as file:
        for line in file:
            lines.append(line.strip())
    return lines


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
        # Use the updated regex pattern
        match = re.search(r'\./Data\\(.*)', df_name)
        if match:
            df['study_name'] = match.group(1)
        else:
            df['study_name'] = 'default_value'


# Concatinate dataframes in dict into single dataframe: 
def concatinate_dfs(df_dict):
    dfs = []
    for df in df_dict.values():
        dfs.append(df)
        concatinated_df = pd.concat(dfs, ignore_index = True)
    
    return concatinated_df


  # DATA HARMONIZATION FUNCTIONS
#---------------------------------------------------------------

# Check if column_names.txt file exists or not
def check_column_names_file():
    file_name = 'column_names.txt'
    if os.path.isfile(file_name):
        return True
    else:
        return False

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
    

### TO BE REMOVED ###
# WRITE text file 
def write_txt_file(text_body, output_file_path):
    try:
        with open(output_file_path, 'w') as text_file:
            text_file.write(text_body)
    except Exception as e:
        print(f"Error occurred while writing to the text file: {e}")
### TO BE REMOVED ###


# PARSE column_name_harmonization.txt
def parse_column_name_harmonization(file_path):
    parsed_dict = {}
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line.startswith('#'):
                parts = line.split('=')
                if len(parts) == 2:
                    key, values = parts
                    key = key.strip()
                    values = [value.strip() for value in values.split(',')]
                    parsed_dict[key] = values
                else:
                    print(f"Ignoring line: {line} - Does not match expected format")

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


# READ MUTATIONS of interest text file
mutations_of_interest_list = read_lines_from_file("mutations.txt")
print("Mutations of interest as specified in file: ")
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
patient_dfs = {}
sample_dfs = {}
mutation_dfs = {}


for df_name in clinical_dfs.keys():
    print(df_name)


# READ DATA tables into dictionary of dataframes
    # Clinical data: 
read_data(data_included, patient_file_name, patient_dfs)
    # Sample data:
read_data(data_included, sample_file_name, sample_dfs)
    # Mutations data: 
read_data(data_included, mutation_file_name, mutation_dfs)


# ADD STUDY NAME as column to dataframes in dictionaries
    # Clinical data: 
add_dataframe_name_column(patient_dfs)
    # Sample data: 
add_dataframe_name_column(sample_dfs)
    # Mutations data:
add_dataframe_name_column(mutation_dfs)



# CONCATINATE DATAFRAMES in dicts into single dataframe
    # Patient data:
all_patient_data = concatinate_dfs(patient_dfs)
=======
# CONCATENATE DATAFRAMES in dicts into single dataframe
    # Clinical data:
all_clinical_data = concatinate_dfs(clinical_dfs)


    # Sample data: 
all_sample_data = concatinate_dfs(sample_dfs)
    # Mutational data:
all_mutations_data = concatinate_dfs(mutation_dfs)





# JOIN clinical- and sample dataframes to single
patient_sample_data = pd.merge(all_patient_data, all_sample_data, on='PATIENT_ID', how='left')


# READ columns of interest txt file
keep_cols = read_lines_from_file("columns_of_interest.txt")
=======
# JOIN clinical- and sample dataframes to single df
patient_sample_data = pd.merge(all_clinical_data, all_sample_data, on='PATIENT_ID', how='left')



duplicates = patient_sample_data[patient_sample_data.duplicated('PATIENT_ID', keep=False)]
duplicates.columns




# FILTER: Keep only columns of interest
patient_sample_data_filtered = patient_sample_data.filter(keep_cols)


# HARMONIZE Column names
column_name_synonyms = {}
column_name_synonyms = parse_column_name_harmonization("column_names_config.txt")


for new_column_name, synonyms in column_name_synonyms.items():
    for synonym in synonyms:
        if synonym in patient_sample_data_filtered.columns:
            patient_sample_data_filtered.rename(columns={synonym: new_column_name}, inplace=True)


# Group by column name and sum the values
merged_df = patient_sample_data_filtered.groupby(patient_sample_data_filtered.columns, axis=1).sum()


print(merged_df)

### TEMP ###
# Get column names
colnames = merged_df.columns.tolist()
### TEMP ###

### TEMP COLUMN INVESTIGATION


# Is NONSYNONYMOUS_MUTATION_BURDEN the same as TMB? --> No

tmp_df = merged_df[['NONSYNONYMOUS_MUTATION_BURDEN', 'TMB']]

merged_df['SAMPLE_CLASS'].describe()
merged_df['TMB'].describe()
merged_df['TMB'].describe()

# OS_MONTHS the same as OS_MONTHS_DMT? --> 
tmp_df = merged_df[['TISSUE_SOURCE_SITE', 'PRIMARY_SITE']]


### TEMP ###


#### STUCK HERE #####

# ADD MUTATION columns

# Add column for each mutation in mutations list. 
for mutation in mutations_of_interest_list:
    patient_sample_data[mutation] = 'WT'
    

# Create a mask for the rows of interest in all_mutations_data
mask = all_mutations_data['Hugo_Symbol'].isin(mutations_of_interest_list)

# Filter rows in all_mutations_data and extract relevant columns
filtered_mutations_data = all_mutations_data.loc[mask, ['Tumor_Sample_Barcode', 'Hugo_Symbol', 'Consequence']]    

for index_ps, row_ps in patient_sample_data.iterrows():
    for index_mut, row_mut in all_mutations_data.iterrows():
        if ow_ps['SAMPLE_ID'] == row_mut['Tumor_Sample_Barcode']:
            


# FIRST FILTER dataset

for index_mut, row_mut in all_mutations_data.iterrows():
    mut_sampleid = row_mut['Tumor_Sample_Barcode']
    hugo_symbol = row_mut['Hugo_Symbol']
    consequence = row_mut['Consequence']
    
    for index_ps, row_ps in patient_sample_data.iterrows():
        if hugo_symbol in mutations_of_interest_list:
            if row_ps['SAMPLE_ID'] == mut_sampleid:
                row_ps[hugo_symbol] = consequence
            

# From ChatGPT: 


# Merge the filtered data into patient_sample_data based on SAMPLE_ID and Hugo_Symbol
merged_data = patient_sample_data.merge(filtered_mutations_data, how='left', left_on='SAMPLE_ID', right_on='Tumor_Sample_Barcode')

# Update the columns in patient_sample_data with non-null values from Consequence
for gene in mutations_of_interest_list:
    mask = merged_data['Hugo_Symbol'] == gene
    patient_sample_data[gene].update(merged_data.loc[mask, 'Consequence'])


#### STUCK HERE #####^
            



# DATA HARMONIZATION
#---------------------------------------------------------------

###  DATA INVESTIGATION  ###
###  DATA INVESTIGATION  ###
# Columns of interest
print(patient_sample_data['PED_IND'])

null_count = patient_sample_data['PED_IND'].isnull().sum()
print(null_count)
###  DATA INVESTIGATION  ###
###  DATA INVESTIGATION  ###




###  DEV HERE  ###
###  DEV HERE  ###
###  DEV HERE  ###
###  DEV HERE  ###




    
###  DEV HERE  ###
###  DEV HERE  ###
###  DEV HERE  ###
###  DEV HERE  ###




#### OLD CODE BELOW #####
#### OLD CODE BELOW #####
#### OLD CODE BELOW #####
#### OLD CODE BELOW #####




#--------------------------------

# APPLY changes
#-------------------------------


# STEP 3: Get input for categories harmonization
#----------------------------------------------

# WRITE categorical entries for each column to a text file:
write_categorical_columns_to_file(patient_sample_df_colnames_harmonized, "categories_harmonization.txt")


# DEFINE column names config string
categories_harmonization_string = "# Please define the categories that represent the same information in this text file following the example rows below, excluding hashes\n"
categories_harmonization_string = categories_harmonization_string + '# "SMOKING_STATUS": "SMOKER"="YES", "NO"="NON-SMOKER"="N"\n'
categories_harmonization_string = categories_harmonization_string + '# "SEX": "MALE"="M"="male", "FEMALE"="F"="female"'

# WRITE column name harmonization txt file
write_txt_file(categories_harmonization_string, "column_name_harmonization.txt")

# WAIT for user to provide input
wait_for_confirmation()

# APPLY changes
#-------------------------------




#===============================================================
# EXECUTE FUNCTIONS: WRITE DATASET MODULE
#===============================================================


# KEEP only RELEVANT columns in mutations data:
all_mutations_data = all_mutations_data[['Tumor_Sample_Barcode', 'Hugo_Symbol', 'Consequence', 'Mutation_Status']]

# FILTER: KEEP only genes defined in GENES OF INTEREST LIST
mutations_data = all_mutations_data[all_mutations_data['Hugo_Symbol'].isin(mutations_of_interest_list)]


# Add column for each mutation in mutations list. 
for mutation in mutations_of_interest_list:
    patient_sample_data[mutation] = 'WT'

# Add mutations of interest data 
for index, row in patient_sample_data.iterrows():
    if row['SAMPLE_ID'] == all_mutations_data['Tumor_Sample_Barcode']:
        tempvar = all_mutations_data['Hugo_Symbol']
        patient_sample_data[tempvar] = all_mutations_data['Consequence']


# Remove duplicate patient data
duplicate_mask = patient_sample_data.duplicated(subset='column_name', keep=False)  # keep=False marks all duplicates as True
result_df = patient_sample_data[duplicate_mask]


# Export dataset to csv
result_df.to_csv('output_file.txt', sep='\t', index=False)


