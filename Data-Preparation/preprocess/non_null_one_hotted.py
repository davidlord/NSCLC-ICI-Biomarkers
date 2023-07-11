from typing import Tuple

# Import packages:
from datetime import datetime
from functools import reduce
import os
import re
import pandas as pd
import glob

os.getcwd()

from .main_preprocess import split_data

GENERAL_LIST_TO_REMOVE = [
    "MSI",
    "Patient_ID",
    "Sequencing_type",
    "PFS_months",
    "TMB_norm",
    "TMB",
    "Immunotherapy",
    "study_name",
    "PD-L1_Expression"
]

GENETIC_LIST_TO_REMOVE = [
    "NFKBIA",
    "NOTCH2",
    "ERBB4",
    "ASXL1",
    "MET",
    "CIC",
    "TET1",
    "PGR",
    "PIK3C2G",
    "NUF2",
    "PTPRD",
    "EPHA7",
    "MAX",
    "JAK3",
    "ABL1",
    "MDC1",
    "EPHB1",
    "INHBA",
    "PIK3C3",
    "PIM1",
    "BRIP1",
    "PPM1D",
    "CDC73",
    "TENT5C",
    "ATM",
    "FGFR4",
    "PARP1",
    "FOXL2",
    "MED12",
    "ZFHX3",
    "EPHA3",
    "TSC2",
    "MGA",
    "RET",
    "EPHA5",
    "NTRK3",
    "STAT3",
    "CD79B",
    "MRE11",
    "PPP2R1A",
    "NF2",
    "PAX5",
    "NOTCH1",
    "BRCA2",
    "HGF",
    "BCOR",
    "ERCC4",
    "CARD11",
    "PIK3CG",
    "FLT3",
    "POLE",
    "KEAP1",
    "KRAS",
    "POLD1",
    "STK11",
    "TP53",
    "MSH2",
    "EGFR",
    "PTEN",
]

def process(config: dict, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Apply 'Main preprocess' to the original data and then transforms the data to numerical by:
        - dropping all rows with null (nan) values
        - creating dummy (one hot encoded) variables of any categorical data.

    (This preprocess is based on PREPROCESSING in feature_engineering_preprocessing.R
    in David Lords original repository https://github.com/davidlord/Biomarkers-immuno-lungcancer.)

    Arguments:
        config -- The preprocess configuration,
        df -- The original data.

    Returns:
        A tuple with the training and test data sets as pandas data frames.
    """
     # add together user columns and specified
    exclude_cols_general = config["general_cols_rm"]
    exclude_cols_genetic = config["genetic_cols_rm"]
    GENERAL_COLS_TO_REMOVE = [exclude_cols_general+GENERAL_LIST_TO_REMOVE]
    GENETIC_COLS_TO_REMOVE = [exclude_cols_genetic+GENETIC_LIST_TO_REMOVE]
    #  column selection.
    print("Selecting columns..")
    columns_to_keep = [column for column in df.columns if column not in GENERAL_COLS_TO_REMOVE+GENETIC_COLS_TO_REMOVE]
    if set(df.columns) != set(columns_to_keep):
        df = df[columns_to_keep]
    else:
        print("No column names match any in the list.")
   
    exclude = config["studies_to_exclude"]
    print(f"Exluding studies: {exclude}")
    df = df.loc[~df["study_name"].isin(exclude)]
    # Drop nan values.
    print("\n---Summarising data before removing nulls.---")
    df.info(memory_usage=False) # Prints info.
    df = df.dropna(how="any", axis=0)
    print("\n\n---Summarising data after removing nulls.---")
    df.info(memory_usage=False) # Prints info.


    # Create dummy variables (one hot encoding) by finding columns in df that are categorical.
    print("\n\n---Creating dummy (one hot encoded) variables.---")
    cat_cols = df.select_dtypes(include=["object"]).columns.tolist()
    
    df = pd.get_dummies(
        df,
        columns=cat_cols,
        prefix='',
        prefix_sep='',
        drop_first=True,
    )

    print("\n---Summarising data after creating dummy variables.---")
    df.info(memory_usage=False) # Prints info.
    print("\n")

    return split_data(df, config)
