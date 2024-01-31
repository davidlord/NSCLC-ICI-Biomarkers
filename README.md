# NSCLC-ICI-Biomarkers

## Background
The identification of certain biomarkers that correlate with immunotherapy treatment outcomes has played a crucial role in guiding the appropriate use of immunotherapies in NSCLC. These biomarkers can provide valuable insights into the likelihood of a patient responding positively to immunotherapy, allowing for more personalized treatment plans and improved therapeutic outcomes. However, the successful integration of biomarker-driven precision oncology relies on the analysis and interpretation of vast and complex datasets, which can be challenging for traditional methodologies. Given this challenge, we aim to in this project deliver a framework to:
1) Deliver a framework for subject matter experts to compile multiple dataset into a single sensible dataset ready for analysis and modelling.
2) Create predictive models of patient treatment outcomes given the input data.

We will in this project focus on datasets of NSCLC patients who have undergone immunotherapy.

## Package Overview
This code repository contains two main processes: "Data-Preparation" and "Modelling". The function of each of these is explained below. 

### Data Preparation
Framework for compiling and preparing cancer genomics datasets from the cBioPortal. Source code compiles multiple separate datasets to a single analysis-ready dataset. Output dataset can be used as input for the "Modelling" framework in this repository. 

### Modelling
A framework for creating a predictive model of NSCLC immunotherapy treatment outcome. XGBoost classification model predicting whether patients are responders or non-responders given the data. 

## Requirements

* Unix-like operating system (Linux, macOS, etc)
* Java >=11
* Conda or Docker

## Repository structure

The repository has several parts to it.
- The **main.nf**. Run module scripts through series of nextflow processes.
- The **nextflow.config**. Look here to find the configuration files and variables used throughout pipeline.
- The **Data** folder. The original data should be stored here under its own unique project folder (ex:  Data/my_unique_project/ ).
- The **conda.yml** contains conda requirements for pipeline.
- **bin** contains most of code implementation. Implement new models, plots, and metrics here.

This package can be run using the default settings or without the different modules (fetch_datasets, preprocess_datasets, etc. ).

For example to skip fetching datasets:

```
--fetch_datasets=false
```

## Entry points
The entry points are executed from the repository root folder using the terminal. Each of them needs some required input (e.g. the path to the corresponding configuration file), which is specified using flags. Which inputs and which flags that should be used to provide the input is specified below and in each entry point's help statement. Access the help statement using the terminal command
 `python <entry point name>.py --help`.

After running an entry point, the resulting output is saved in a specified folder together witn any used configuration and the git info.

### Fetching data

The *fetch data* module involves data cleaning, feature engineering, and harmonization of input datasets and specified mutation data. 

Available flags

The user specifies the type of data to include, --datatype="categorical" or --datatype="numerical" for config generation. 

The datasets to include are specified via the command line with the flag --dataset_names shown below:

``` --dataset_names my_own_project,luad_mskcc_2015,luad_mskcc_2020 ```

The default 'mutations.txt' is used to create the data set for downstream processing but can also be specified with the flag --mutations
shown below:

``` --mutations my_own_project_mutations.txt ```

If you would like to include your own list of mutations simply modify the mutations.txt file by adding your own line to the end of the file given the following format:

``` 
MY_MUTS_EXAMPLE = [mut1, mut2_example, etc]
```


### Preprocessing data
The *preprocess* module imports the raw data from a .csv formatted file and prepares it for training and testing models, using the specification in its corresponding configuration file. 

The preparation involves data cleaning, feature engineering, and splitting into test and train data sets. What kind of the preparations that is done can be changed by specifying a different preprocessor in the configuration file.

Available flags
```
--remove_cols
```

### Training

The training module trains a model with specified parameters on a preprocessed data set according to the details specified in its corresponding configuration file.

### Prediction/Inference

The prediction module uses a model to evaluate a test data set. After the inference, the result is saved in a folder specified when executing the entry point.

Available flags

```
--data_path (Path to the test data on which to run evaluation.)
--output_file (Path to the filename to save prediction/inference data.)
```

### Analyisis
The entry point *analyze.py* creates various plots and computes measures on both the original data and on the inference of a model. If the used model supports it, it can also give some information about the model. The output is saved in a folder specified when executing the entry point.

Available flags

```
--experiment_folder (Path to the folder of the trained model saved on disk.)
--output_path (Path to the data on which to run evaluation.)
```


## Quickstart 

```
nextflow run main.nf --profile conda --datatype "categorical" --model_type=xgboost
```
