#!/usr/bin/env python3

from typing import Tuple
import pandas as pd
import os
from datetime import datetime
from sklearn.model_selection import train_test_split

cwd=os.getcwd().split('work', 1)[0]

def main_process_module(config: dict, df: pd.DataFrame, *args) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Apply 'Main preprocess' to the original data.

    Arguments:
        config -- The preprocess configuration.
        df -- The original data.

    Returns:
        A tuple with the training and test data sets as pandas data frames.
    """
    # column selection.
    if args:
        print("Selecting columns..")
        df = df.drop(columns=args.remove_cols, axis=1, inplace=False)
    else:
        pass
    return split_data(df, config)


def split_data(data: pd.DataFrame, config: dict) -> Tuple[pd.DataFrame, pd.DataFrame]:
    test_set_size = config["test_set_size"]

    print(
        f"Splitting the data {int((1-test_set_size)*100)}/{int(test_set_size*100)} for training/test set. "
    )
    train, test = train_test_split(
        data, test_size=test_set_size, random_state=config["random_seed"]
    )

    # Reset any indices before return.
    return train.reset_index(drop=True), test.reset_index(drop=True)


