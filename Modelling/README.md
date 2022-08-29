# Introduction

This code was designed with the following in mind:

- It should be easy to run different setups **without changing any code**.
- Each model training or data preprocessing should be **reproducible**.
- Save all relevant output from preprocessing, model training, inference, and analysis in a structured manner.

Therefore, the repository is based around a few entry point which are configured (mainly) using configuration files. This means that different combinations of preprocesses, models, and model parameters can be tried by **only changing configuration files**. After running an entry point, the result is then saved along with the results along with the configuration and the state of source code (using a git commit id). See existing example config files for more details.

### **Example: preprocessing**

  - Create or modify a preprocessing config file.
    - Specify which preprocessor to use.
    - Specify which original data file to use.
  - Run preprocessing entry point with the config file as input.
  - The resulting preprocessed data is saved in a new subfolder located under `data/preprocessed/`. The name of the subfolder is derived from the config file and the current date time. This folder contains:
    - The `train_data.csv` and `test_data.csv` files.
    - A copy of the configuration file.
    - A identifier of the source code state (the `git_info.txt`).

  - The copied config file and git identifier can later be used to recreate the data from the original data.

### **Example: model training**

  - Create or modify a model config file.
    - Specify which preprocessed data to train on. **This should point to the train_data.csv file created in the preprocessing step!**
    - Specify which model to use and any model parameters.
  - Run training entry point using the configuration.
  - The resulting model is saved together with a copy of the config file and an identifier of the source code state (the `git_info.txt`).
  - The copied configuration, identifier and preprocessed data can later be used to recreate the model.

## Repository structure
The repository has several parts to it.
- The **entry points**. These are Python files placed in the root folder that are used to run various parts of the code using a terminal.
- The **config folder**. Look here to find the configuration files used when running the code.
- The **data folder**. The original data should be stored here and the preprocessors saves processed data here.
- The **preprocess folder** contains the code for preprocessing. Implement new preprocessors to this folder.
- The **setup folder** contains a script for installation and setting up the repository.
- The **src folder** contains most of code implementation. Implement new models, plots, and metrics here.

# Installation

## The Python virtual environment (venv)

A Python virtual environment is local sandbox which makes sure that there is no conflicts between the potentially different packages and package versions required for the different projects.

## How to install and use on Linux

Run the setup.sh script in the setup folder to create a new Python working environment and install all Python packages needed.

From the root of the project:

```bash
$ ./setup/setup.sh
```

After installation is complete, run the following to activate the virtual environment.

```bash
$ source venv/bin/activate
```

You should now be able to run the python scripts in the project. 

To deactivate the environment by running `$ deactivate`.

## How to install and use on Windows

Make sure that your user is allowed to run scripts (or proceed to the next step and keep an eye out for the error message in case you do need to allow running scripts).
Open a terminal in the root folder of the project and run the following. If you're unsure how to open a terminal see the section [How to use the terminal](#how-to-use-the-terminal) further down

```
.setup/setup.sh
```

### How to activate the environment

In the terminal, execute `.\venv\Scripts\activate`. Is sucessfull '*(venv)*' should be preprended to the path (see image below).

![Activating venv](assets\activate_venv.PNG "Activate venv")

### How to deactivate

Execute  `deactivate` in the terminal. The '*(venv)*' prefix should disappear from the terminal line.

### How to use the terminal

- In the windows explorer, open the repository root folder (the folder where this readme is located).
- Right click and select 'Open terminal'. This should open a Windows PowerShell terminal or an equivalent terminal.
- Run the various commands specified the different steps. (All scripts should be executed standing in the repository root folder.)

# Using the repository

As mentioned, usage of the repository is based around executing entry points which are configured (mainly) using configuration files. There are four entry points: *preprocess.py, train.py, infer.py, and analyze.py*.

## Prerequisites
- Make sure that Python 3 is installed.
- Put the original data file in the data folder. 
  - Make it read-only. Best practice is to never change the original data to ensure reproducibility.
- Open a terminal in the root folder. When executing the various entry points and scripts, always start from the repository root folder (where this README is located). 
- Set up and **activate** the Python virtual environment together with the required packages (see [The Python virtual environment](./README.md#The-Python-virtual-environment-(venv)).

## Entry points
The entry points are executed from the repository root folder using the terminal. Each of them needs some required input (e.g. the path to the corresponding configuration file), which is specified using flags. Which inputs and which flags that should be used to provide the input is specified below and in each entry point's help statement. Access the help statement using the terminal command
 `python <entry point name>.py --help`.

After running an entry point, the resulting output is saved in a specified folder together witn any used configuration and the git info.

### Preprocessing data
The entry point *preprocess.py* imports the raw data from a .csv formatted file and prepares it for training and testing models, using the specification in its corresponding configuration file. The preparation involves data cleaning, feature engineering, and splitting into test and train data sets. What kind of the preparations that is done can be changed by specifying a different preprocessor in the configuration file.

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

