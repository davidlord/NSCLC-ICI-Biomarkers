#!/usr/bin/env python3

import os
import re
import glob
import pandas as pd
from pathlib import Path
from typing import Tuple
from datetime import datetime
from functools import reduce
from utils import prepare_save_folder, read_config

from non_null_one_hotted import nn_process
from main_preprocess import main_process_module

DATA_FOLDER = Path("Modelling/data/preprocessed")

class Preprocessor:
    """Preprocess the data to be used with the models.

    Public methods:
    process -- Loads the data from file, processes it, and saves the results.

    Instance variables:
    config -- The preprocess config
    preprocessor_type -- The name of the preprocessor to use.
    """

    def __init__(self, config_path: Path) -> None:
        """Initialize the processor.
        Arguments:
            config_path -- The path to the configuration file.
        """
        self.config = read_config(config_path)
        self.preprocessor_type = self.config["preprocessor_name"]

    def _load_data(self) -> pd.DataFrame:
        """Load orignal data from disk."""
        return pd.read_csv(self.config["data_path"], sep="\t", header=0, engine='python')


    def _save(self, train_data: pd.DataFrame, test_data: pd.DataFrame) -> None:
        """Save the preprocessed data to disk as a training and test sets.

        Arguments:
            train_data -- The training data set.
            test_data -- The test data set.
        """
        # Prepare save folder.
        preproc_output = prepare_save_folder(
            DATA_FOLDER,
            self.config["output_name"],
            ["config", "data"],
            {"preprocess_config": self.config},
        )

        # Save data.
        train_data.to_csv(preproc_output / "train_data.csv", index=False)
        test_data.to_csv(preproc_output / "test_data.csv", index=False)
        print(f"Saved processed data to {preproc_output}")

    def _preprocess(self, data) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Apply the preprocessor specified in the configuration to the data.

        Arguments:
            data -- The data to preprocess.

        Returns:
            A tuple with the training and test data sets.
        """
        if self.preprocessor_type == "main_preprocessor":
            train_dataset, test_dataset = main_process_module(self.config, data)
        elif self.preprocessor_type == "non_null_one_hotted":
            train_dataset, test_dataset = nn_process(
                self.config, data, 
            )
        else:
            assert False, "No preprocessor found!"
        return train_dataset, test_dataset

    def process(self) -> None:
        """Load the data from file, process it, and save the results."""
        print("Loading original data set..")
        data = self._load_data()
       # print("Processing..", data.head())
        train_data, test_data = self._preprocess(data)
        print("Saving processed data..")
        self._save(train_data, test_data)

