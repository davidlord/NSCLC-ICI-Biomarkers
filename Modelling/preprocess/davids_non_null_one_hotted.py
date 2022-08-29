from typing import Tuple

import pandas as pd

from .davids_preprocess import split_data

GENERAL_COLS_TO_REMOVE = [
    "MSI",
    "Patient_ID",
    "Sequencing_type",
    "PFS_months",
    "Stage_at_diagnosis",
    "TMB_norm",
    "TMB",
    "Pan_2020_muts",
    "Immunotherapy",
]

GENETIC_COLS_TO_REMOVE = [
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
    """Apply 'Davids preprocess' to the original data and then transforms the data to numerical by:
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

    exclude = config["studies_to_exclude"]
    print(f"Exluding studies: {exclude}")
    df = df.loc[~df["Study_ID"].isin(exclude)]

    print("Selecting columns..")
    df = df.drop(columns=GENERAL_COLS_TO_REMOVE, axis=1, inplace=False)
    df = df.drop(columns=GENETIC_COLS_TO_REMOVE, axis=1, inplace=False)

    # Drop PD-L1_Expression info.
    df.drop(columns=["PD-L1_Expression"], axis=1, inplace=True)

    # Drop nan values.
    print("\n---Summarising data before removing nulls.---")
    df.info(memory_usage=False) # Prints info.
    df = df.dropna(how="any", axis=0)
    print("\n\n---Summarising data after removing nulls.---")
    df.info(memory_usage=False) # Prints info.

    # Create dummy variables (one hot encoding).
    print("\n\n---Creating dummy (one hot encoded) variables.---")
    df = pd.get_dummies(
        df,
        columns=["Study_ID", "Histology", "Smoking_History", "Sex"],
        prefix=["Study", "Histology", "Smoking", "Sex"],
        drop_first=True,
    )

    print("\n---Summarising data after creating dummy variables.---")
    df.info(memory_usage=False) # Prints info.
    print("\n")

    return split_data(df, config)
