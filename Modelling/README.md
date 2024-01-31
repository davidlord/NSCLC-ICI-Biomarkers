# Introduction

This code was designed with the following in mind:

- It should be easy to run different setups **without changing any code**.
- Each model training or data preprocessing should be **reproducible**.
- Save all relevant output from preprocessing, model training, inference, and analysis in a structured manner.

Therefore, the repository is based around a few entry point which are configured (mainly) using configuration files. This means that different combinations of preprocesses, models, and model parameters can be tried by **only changing configuration files**. After running an entry point, the result is then saved along with the results along with the configuration and the state of source code (using a git commit id). See existing example config files for more details.

## Repository structure
The repository has several parts to it.
- The **main.nf**. Run module scripts through series of nextflow processes.
- The **nextflow.config**. Look here to find the configuration files and variables used throughout pipeline.
- The **Data** folder. The original data should be stored here under its own unique project folder (ex:  Data/my_unique_project/ ).
- The **conda.yml** contains conda requirements for pipeline.
- **bin** contains most of code implementation. Implement new models, plots, and metrics here.

## Installation

- The main requirements are nextflow version >= 23.04.3 and java version >= jdk19.0.2

## Prerequisites

- Put original data in the *Data* under an individually named project folder with the following specifications:
    - Data/my_unique_project/data_clinical_patient.txt : which can contain column names similar to those provided in the test datasets for example:
      - PATIENT_ID, SEX , AGE ,SMOKER , TREATMENT_TYPE, PFS_STATUS, DURABLE_CLINICAL_BENEFIT
      - minimally : PATIENT_ID, SMOKER or SMOKING HISTORY, PFS_STATUS
    - Data/my_unique_project/data_mutations.txt which can contain column names similar to those provided in the test datasets for example:
      - Hugo_Symbol , Entrez_Gene_Id , Chromosome,  Start_Position , End_Position, Consequence , Tumor_Sample_Barcode    Matched_Norm_Sample_Barcode , Tumor_Validation_Allele2 ,  Mutation_Status
      - minimally: Hugo_Symbol, Tumor_Sample_Barcode
    - Data/my_unique_project/data_clinical_sample.txt : which can contain column names similar to those provided in the test datasets for example:
      - PATIENT_ID , SAMPLE_ID , GENE_PANEL , PDL1_SCORE , TMB_NONSYNONYMOUS
      - minimally : PATIENT_ID , SAMPLE_ID , TMB or TMB_NONSYNONYMOUS

## Entry points
The entry points are executed from the repository root folder using the terminal. Each of them needs some required input (e.g. the path to the corresponding configuration file), which is specified using flags. Which inputs and which flags that should be used to provide the input is specified below and in each entry point's help statement. Access the help statement using the terminal command
 `python <entry point name>.py --help`.

After running an entry point, the resulting output is saved in a specified folder together witn any used configuration and the git info.

### Fetching data

The *fetch data* module involves data cleaning, feature engineering, and harmonization of input datasets and specified mutation data. 

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

**How to run in the terminal**

```python preprocess.py -c <path to configuration file>```

**Available flags**
- ```--help```
- `-c` or `--config_path` (Path to preprocess config file, typically located under `configs/preprocess/`)

### Training a model
The entry point *train.py* train a model with specified parameters on a preprocessed data set according to the details specified in its corresponding configuration file.


**How to run in the terminal**

```python train.py -c <path to configuration file>```

**Available flags**
- ```--help```
- `-c` or `--config_path` (Path to model config file, typically located under `configs/models/`)

### Running inference
The entry point *infer.py* uses a model to evaluate a test data set. After the inference, the result is saved in a folder specified when executing the entry point.

**How to run in the terminal**

```python infer.py -c <path to configuration file>```

**Available flags**
- ```--help```
- `-exp` or `--experiment_folder` (Path to the folder of the trained model saved on disk.)
- `-d` or `--data_path` (Path to the data on which to run evaluation.)
- `-o` or `--output_path` (Path to the data on which to run evaluation.)

### Running analyisis
The entry point *analyze.py* creates various plots and computes measures on both the original data and on the inference of a model. If the used model supports it, it can also give some information about the model. The output is saved in a folder specified when executing the entry point.

**How to run in the terminal**

```python analyze.py -ac <path to configuration file> -exp <path to folder containing model> -o <path to the data to analyze>```

**Available flags**
- ```--help```
- `-ac` or `--analysis_config` (Path to plotting config file, typically located under `configs/analysis/`)
- `-exp` or `--experiment_folder` (Path to the folder of the trained model saved on disk.)
- `-o` or `--output_path` (Path to the data on which to run evaluation.)

