#!/usr/bin/env python3

import sys
import argparse
import os
import json
import glob
#import ruamel.yaml
#from ruamel.yaml.scalarstring import SingleQuotedScalarString, DoubleQuotedScalarString
#from datetime import datetime
from pathlib import Path
from preprocessor import Preprocessor
#from utils import read_config, get_current_datetime

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

    main(sys.argv[2])

  #  config_to_load = read_config(args.config_path)
  #  output_name = config_to_load['output_name']

#    start_time = datetime.now().strftime("%Y%m%d-%H%M")
 #   latest_file = os.path.join(cwd, args.outdir,'Modelling','data','preprocessed',output_name+'_'+start_time,'data','train_data.csv')

  #  yaml = ruamel.yaml.YAML()

   # if args.model_type == "xgboost":
    #    yml_dict = \

                #training_name: xgboost_model
                #random_seed:    
                #model: xgboost  
                #args: {
                 #        tree_method: hist,
                  #       enable_categorical: True
                  #      }
               # preprocessed_data_path:
               # gt_column: "PFS_STATUS"
       # """
        #yaml.preserve_quotes = True
        #yaml.explicit_start = True
        #yaml_dump = yaml.load(yml_dict)
        #yaml_dump['random_seed'] = config_to_load['random_seed']
        #yaml_dump['preprocessed_data_path'] = latest_file
        #with open("xgboost_model_config.yml", 'w') as f:
         #   yaml.dump(yaml_dump, f)
    #else:
     #   yml_dict = { 'training_name': "keras_feed_forward", # Training info
      #          'random_seed': config_to_load['random_seed'], # sets seed for model initiation
       #         'model': "keras_feed_forward" , # Model info
        #        'args': { 
         #               'nr_of_epochs': 130,
          #              'optimizer': "adam",
           #             'loss': "binary_crossentropy", 'metrics': ["accuracy", "mean_squared_error"], # Configure the model architecture.
            #            'layers': [ # Only dense layers are supported currently.
             #                     {
             #                       'type': "dense",
              #                      'size': 1,
               #                     'activation': "relu"},
                #                  {'type': "dense", 
                 #                  'size': 10, 
                  #                 'activation': "relu"},
                   #               {'type': "dense" , 
                      #             'size': 1, 
                    #               'activation': "sigmoid"
                     #             } 
                      #            ] 
                       # }, # For binary classification the final layer must be size 1 with sigmoid activation.
            # 'preprocessed_data_path': latest_file,
            # 'gt_column': "PFS_STATUS" }
        #json_string = json.dumps(yml_dict)
        #data = yaml.load(json_string)
        # the following sets flow-style for the root level mapping only
       # data.fa.set_block_style()
       # with open("keras_model_config.yml", 'w') as f:
        #    yaml.dump(yml_dict, f)




