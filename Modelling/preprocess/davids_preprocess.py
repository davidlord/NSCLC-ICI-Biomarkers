from typing import Tuple

import pandas as pd
from sklearn.model_selection import train_test_split

GENERAL_COLS_TO_REMOVE = [
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
    """Apply 'Davids preprocess' to the original data.

    (This preprocess is based on PREPROCESSING in feature_engineering_preprocessing.R
    in David Lords original repository https://github.com/davidlord/Biomarkers-immuno-lungcancer.)

    Arguments:
        config -- The preprocess configuration.
        df -- The original data.

    Returns:
        A tuple with the training and test data sets as pandas data frames.
    """

    exclude = config["studies_to_exclude"]
    print(f"Exluding studies: {exclude}")
    df = df.loc[~df["Study_ID"].isin(exclude)]

    # Davids column selection.
    print("Selecting columns..")
    df = df.drop(columns=GENERAL_COLS_TO_REMOVE, axis=1, inplace=False)
    df = df.drop(columns=GENETIC_COLS_TO_REMOVE, axis=1, inplace=False)

    # Drop PD-L1_Expression info
    df.drop(columns=["PD-L1_Expression"], axis=1, inplace=True)

    return split_data(df, config)


def split_data(data: pd.DataFrame, config: dict) -> Tuple[pd.DataFrame, pd.DataFrame]:
    test_set_size = config["test_set_size"]

    print(
        f"Splitting the data {int((1-test_set_size)*100)}/{int(test_set_size*100)} for training/test set. "
    )
    train, test = train_test_split(
        data, test_size=test_set_size, random_state=config["random_seed"]
    )
    train["Treatment_Outcome"].replace(
        {"Non-Responder": 0, "Responder": 1}, inplace=True
    )
    test["Treatment_Outcome"].replace(
        {"Non-Responder": 0, "Responder": 1}, inplace=True
    )

    # Reset any indices before return.
    return train.reset_index(drop=True), test.reset_index(drop=True)
