import argparse
from pathlib import Path

from src.trainer import Trainer
from src.utils import check_git_status


def main(config_path: Path) -> None:
    check_git_status()
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
        "-c",
        "--config_path",
        required=True,
        type=Path,
        help="Path to model config file.",
        default="config/model/xgboost_model_config.yml",
    )
    args = vars(parser.parse_args())

    main(**args)
