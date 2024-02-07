#!/usr/bin/env python3

import os
import argparse
from pathlib import Path
from typing import Optional

from analyzer import Analyzer

cwd=os.getcwd().split('work', 1)[0]

def main(
    analysis_config: Path,
    experiment_dir: Path,
    data_path: Optional[Path] = None
) -> None:
    print('exp directory', experiment_dir)
    model_config_path = experiment_dir
    print('model_config_path ', model_config_path)
    pathlist = os.path.dirname(model_config_path).split('/')[:-1]
    pathlist = ['/' if x == '' else x for x in pathlist]
    print('pathlist', pathlist)
    output_path = os.path.join(*pathlist, "analysis" )
    model_path = os.path.join(*pathlist , "model")
    print('model_path', model_path)
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
        "--analysis_config",
        type=Path,
        help="Path to analysis config file."
    )
    parser.add_argument(
        "--experiment_dir",
        type=Path,
        required=False,
        help="Path to the experiment folder of the trained model."
    )
    parser.add_argument(
        "--data_path",
        type=Path,
        help="Path to the data on which to run the analysis.",
    )

    args = vars(parser.parse_args())

    main(**args)
