import argparse
from pathlib import Path
from typing import Optional

from src.trainer import Trainer


def main(experiment_folder: Path, data_path: Path, output_file: Path) -> None:
    assert output_file.suffix == ".csv", "ERROR: Output file does not have `.csv` extension! Exiting."
    model_config_path = experiment_folder / "config/model_config.yml"
    model_path = experiment_folder / "model"
    trainer = Trainer(model_config_path, resume_model=model_path, data_path=data_path)
    trainer.predict(output_file)


if __name__ == "__main__":
    # Parse command line arguments.
    parser = argparse.ArgumentParser(
        description="Script to load a previously trained model and perform"
        "prediction on given data.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-exp",
        "--experiment_folder",
        type=Path,
        required=True,
        help="Path to the experiment folder of the trained model.",
    )
    parser.add_argument(
        "-d",
        "--data_path",
        type=Path,
        help="Path to the data (.csv file) on which to run prediction.",
    )
    parser.add_argument(
        "-o",
        "--output_file",
        type=Path,
        required=True,
        help="Path to file where to save the output data with predictions. "
        "Must end with `.csv`.",
    )
    args = vars(parser.parse_args())

    main(**args)
