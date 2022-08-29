import argparse
from pathlib import Path
from typing import Optional

from src.analyzer import Analyzer


def main(
    analysis_config: Path,
    experiment_dir: Path,
    data_path: Optional[Path] = None,
) -> None:
    model_config_path = experiment_dir / "config/model_config.yml"
    output_path = experiment_dir / "analysis"
    model_path = experiment_dir / "model"
    analyser = Analyzer(
        analysis_config,
        model_config_path,
        output_path,
        model_path=model_path,
        data_path=data_path,
    )
    analyser.analyse()


if __name__ == "__main__":
    # Parse command line arguments.
    parser = argparse.ArgumentParser(
        description="Script to analyze data and/or model. Results are saved "
        "under <experiment_directory>/analysis/.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-ac",
        "--analysis_config",
        type=Path,
        default="configs/analysis/xgboost_analysis_config.yml",
        help="Path to analysis config file.",
    )
    parser.add_argument(
        "-exp",
        "--experiment_dir",
        type=Path,
        required=True,
        help="Path to the experiment folder of the trained model.",
    )
    parser.add_argument(
        "-d",
        "--data_path",
        type=Path,
        help="Path to the data on which to run the analysis.",
    )
    args = vars(parser.parse_args())

    main(**args)
