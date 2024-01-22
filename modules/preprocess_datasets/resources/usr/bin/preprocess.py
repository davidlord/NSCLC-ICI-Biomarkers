#!/usr/bin/env python3

import sys
import argparse
import os
import yaml
from pathlib import Path
from datetime import datetime
from preprocessor import Preprocessor
from utils import check_git_status

cwd=os.getcwd().split('work', 1)[0]

def main(config_path: Path) -> None:
    #check_git_status()
    preorcessor = Preprocessor(config_path)
    preorcessor.process()


if __name__ == "__main__":
    # Parse command line arguments.
    parser = argparse.ArgumentParser(
        description="Script to prepare data for training or predicton.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--config_path",
        required=True,
        type=Path,
        default=Path(os.path.join(cwd, "${params.output_dir}", "configs/preprocess/preprocess_config.yml")),
        help="Path to preprocess config file.",
    )
    parser.add_argument('--remove_cols', help='names of cols to drop, ex: HISTOLOGY,PFS_MONTHS',required=False, default=None)
    parser.add_argument('--model_type', help='ML model, default: xgboost',required=False, default='xgboost')
    parser.add_argument('--outdir', help='name of output directory, default: outdir',required=False, default='outdir')
    
    args = parser.parse_args()

    if args.model_type == "xgboost":
        config = {
                'training_name': "xgboost_model", # Training info
                'random_seed':  42, # sets seed for model initiation
                'model': "xgboost" , # Model info
            'args': { # Any specific args for the model
                'tree_method': 'hist',
                'enable_categorical': 'true'
                },
        'preprocessed_data_path': os.path.join(cwd, args.outdir,'Modelling','data','preprocessed','data_'+datetime.now().strftime('%b%d%Y')+'-'+datetime.now().strftime('%H%M%S'),'data','train_data.csv'), # Data info
        'gt_column': "PFS_STATUS",
        }
        with open("xgboost_model_config.yml", 'w') as f:
            yaml.dump(config, f)
    else:
        config = {
                'training_name': "keras_feed_forward", # Training info
                'random_seed': 42, # sets seed for model initiation
                'model': "keras_feed_forward" , # Model info
            'args': {
                'nr_of_epochs': 130,
                'optimizer': "adam",
                'loss': "binary_crossentropy",
                'metrics': ["accuracy", "mean_squared_error"],# Configure the model architecture.
                'layers': [ # Only dense layers are supported currently.
                 {
                    'type': "dense",
                    'size': 16,
                    'activation': "relu",
                },
                {
                    'type': "dense",
                    'size': 10,
                    'activation': "relu",
                },
                { # For binary classification the final layer must be size 1 with sigmoid activation.
                    'type': "dense",
                    'size': 1,
                    'activation': "sigmoid"
                }
                ]
            },
        'preprocessed_data_path': os.path.join(cwd, args.outdir,'Modelling','data','preprocessed','data_'+datetime.now().strftime('%b%d%Y')+'-'+datetime.now().strftime('%H%M%S'),'data','train_data.csv'), # Data info
        'gt_column': "PFS_STATUS",
        }
        with open("keras_model_config.yml", 'w') as f:
            yaml.dump(config, f)

    main(sys.argv[2])


