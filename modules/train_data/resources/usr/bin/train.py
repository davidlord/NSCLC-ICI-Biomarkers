#!/usr/bin/env python3


import argparse
from pathlib import Path
import os
from trainer import Trainer
#from utils import check_git_status

cwd=os.getcwd().split('work', 1)[0]

def main(config_path: Path) -> None:
    #check_git_status()
    trainer = Trainer(config_path)
    trainer.train()


if __name__ == "__main__":
    # Parse command line arguments.
    parser = argparse.ArgumentParser(
        description="Script to train a model using preprocessed data. "
        "Model artifacts will be saved to the `output` directory.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--config_path",
        required=True,
        type=Path,
        help="Path to model config file.",
        default=Path(os.path.join(cwd, "${params.output_dir}","configs/models/xgboost_model_config.yml"))
    )
    args = vars(parser.parse_args())

    main(**args)
