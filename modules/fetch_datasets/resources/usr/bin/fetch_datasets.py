#!/usr/bin/env python3

# Import packages:
import argparse
import json
import yaml
import os
import re
import pandas as pd
import glob
import argparse
from datetime import datetime


class FetchData(datasets):
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
    def get_categories(df):
        result = {}
        for c in df.columns:
            if is_categorical(df[c]):
                values = df[c].unique().tolist()
            # fix bug with numerical categories
                if sum(v.isdigit() for v in values) == len(values):
                    values = [int(v) for v in values]
                result[c] = values
        return result


if __name__ == '__main__':
    # parse command-line arguments
    parser = argparse.ArgumentParser(description='Harmonize Datasets')
    ## which studies to use for analysis
    parser.add_argument('--data', help='Which datasets', required=False, default=['luad_mskcc_2015','nsclc_mskcc_2015','luad_mskcc_2020','nsclc_mskcc_2018'])
    # user provided name for each run 
    parser.add_argument('--datatype', help='numerical or categorical', required=True)

    args = parser.parse_args()
    
    datasets = []
    for study in args.data:
        datasets.append(study)
    
    inputdata = FetchData(datasets)

    # save data
    inputdata.frame.to_csv('data_'+datetime.now().strftime('%b%d%Y')+'.tsv' , sep='\t')

    # save config 
    if args.datatype is "categorical":
        config = {
            'preprocessor_name': "non_preprocessor",
            'test_set_size': 0.2 ,# Part of data. 1 is all data.
            'random_seed':  42 ,# sets seed for training/test set splits
            'output_name': "categorical_preprocess",

            'data_path': os.path.join(os.getcwd(),'outdir','DataPrep','data_'+datetime.now().strftime('%b%d%Y')+'.tsv')
        }
        with open("preprocess_config.yml", 'w') as f:
            yaml.dump(config, f)
    else:
        config = {
            'preprocessor_name': "non_null_one_hotted",
            'test_set_size': 0.2, # Part of data. 1 is all data.
            'random_seed': 42, # sets seed for training/test set splits
            'output_name': "numerical_preprocess",

            'data_path': os.path.join(os.getcwd(),'outdir','DataPrep','data_'+datetime.now().strftime('%b%d%Y')+'.tsv')
        }
        with open("numerical_preprocess_config.yml", 'w') as f:
            yaml.dump(config, f)

    # save metadata
    meta = {
        'name': 'data_'+datetime.now().strftime('%b%d%Y'),
        'feature_names': inputdata.feature_names,
        'target_names': inputdata.target_names,
        'categories': get_categories(inputdata.frame) 
    }

    with open("meta.json", 'w') as f:
        json.dump(meta, f)