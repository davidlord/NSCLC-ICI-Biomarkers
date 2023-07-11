import argparse
from pathlib import Path

from preprocess.preprocessor import Preprocessor
from src.utils import check_git_status


def main(config_path: Path) -> None:
    check_git_status()
    preorcessor = Preprocessor(config_path)
    preorcessor.process()


if __name__ == "__main__":
    # Parse command line arguments.
    parser = argparse.ArgumentParser(
        description="Script to prepare data for training or predicton.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-c",
        "--config_path",
        required=True,
        type=Path,
        default=Path("DataAssembly/configs/main_preprocess.yml"),
        help="Path to preprocess config file.",
    )
    args = vars(parser.parse_args())

    main(**args)
