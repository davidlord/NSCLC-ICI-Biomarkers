#!/usr/bin/env nextflow 

/*
 * Copyright (c) 2023, Clinical Genomics.
 * Distributed under the terms of the MIT License.
 */
import groovy.json.JsonSlurper

if(!params.datatype) {
    error("unknown datatype specified --datatype: categorical or numerical")
}

include { fetch_dataset } from './modules/fetch_dataset'
include { visualize } from './modules/visualize'
include { preprocess_datasets } from './modules/preprocess_datasets'
include { train_data} from './modules/train_data'
include { infer_from_data } from './modules/infer_from_data'
include { analyze_dataset } from './modules/analyze_dataset'

log.info """\
        NSCLC-ICI pipeline
        ===============
        fetch_datasets   : ${params.fetch_dataset}
        dataset_names    : ${params.dataset_names}
        datatype    : ${params.datatype}

        visualize	: ${params.visualize}

        mutations_data  : ${params.mutations_data}

        preprocess	: ${params.preprocess}
        preproc_data :  ${params.preproc_data_folder}
        remove_cols :  ${params.cols_to_remove}
        model_type    : ${params.model_type}

        train           : ${params.train}

        predict         : ${params.predict}
        predict_models  : ${params.predict_models}
        predict_train    : ${params.predict_train}
        predict_test    : ${params.predict_test}

        infer_outfile: ${params.infer_outfile}

        analyze         : ${params.analyze}

        output_dir        : ${params.output_dir}
        """
        .stripIndent()

/* 
 * main script flow
 */

process PRINT_PATH {
  debug true
  output:
    stdout
  script:
  """
  echo $PATH
  """
}


workflow {
    mut_file	   = Channel.fromPath("${params.mutations_data}")
    
    // fetch example datasets if none specified
    if ( params.fetch_dataset == true ) {
        // extract gene names from mutations file
        gene_sets = mut_file.flatMap {
            it.readLines().collect { line -> line.tokenize("\t")[0] }
        }

	    mut_file = mut_file.collect()

        (ch_config, ch_data) = fetch_dataset(params.dataset_names, params.datatype, params.mutations_data)
        print(ch_config)
        ch_data.view()
    }
    // otherwise load input files: need DataPrep/*.tsv & config
    else {
        ch_data = Channel.fromPath("${params.output_dir}/DataPrep/*.tsv")
        ch_config = Channel.fromPath("${params.output_dir}/configs/preprocess/*.yml")
    }

    // visualize stats if input data sets
    if ( params.visualize == true ) { 
        visualize(ch_datasets) 
        } 
    // or dont 
    else{    pass  } 

    //  PRINT_PATH()
    // preprocess data sets
    if ( params.preprocess == true ) {
        // if preprocess of dataset needed for categorical processing, creating train/test sets
        (ch_preproc_config, ch_train_config, ch_train_data, ch_test_data)  = preprocess_datasets(ch_config, params.cols_to_remove, params.model_type ) 
        ch_train_config.view()
    } // else load previously generated train, test sets
    else {
        ch_train_config = Channel.fromPath("${params.output_dir}/configs/preprocess/*.yml",  checkIfExists: true )
        ch_train_data = Channel.fromPath("${params.output_dir}/Modelling/data/preprocessed/${params.preproc_data_folder}/data/train_data.csv")
        ch_test_data = Channel.fromPath("${params.output_dir}/Modelling/data/preprocessed/${params.preproc_data_folder}/data/test_data.csv")
        print(ch_train_config)
    }
    

    // print warning if both training and pre-trained model are enabled
    //if ( params.train == true && params.predict_models != null ) {
     //   log.warn 'Training is enabled but pre-trained model(s) are also provided, pre-trained models will be ignored'
    //}

    // perform training if specified
    if ( params.train == true ) {
        (ch_train_model_json, ch_train_model_config) = train_data(ch_train_config)
        ch_train_model_config.view()
        }
    else{
        ch_train_model_config = Channel.fromPath("${params.output_dir}/configs/models/*.yml",  checkIfExists: true )
        ch_train_model_config.view()
        }

    // perform prediction and inference if specified
    if ( params.predict == true ) {

        (ch_infer_csv, ch_config_for_analysis) = infer_from_data(ch_train_model_config, ch_test_data, params.infer_outfile)
        ch_config_for_analysis.view()
    }
    else{
        ch_config_for_analysis = Channel.fromPath("${params.output_dir}/Modelling/output/models/*/config/*.yml",  checkIfExists: true )
        ch_infer_csv = Channel.fromPath("${params.output_dir}/Modelling/output/models/*/inference/*.csv",  checkIfExists: true )
        ch_config_for_analysis.view()
    }

    // perform analysis if specified
    if ( params.analyze == true ) {
        = analyze_dataset(ch_config_for_analysis, ch_infer_csv)
    }
    else{
        "No analysis performed"
    }
}

/* 
 * completion handler
 */
workflow.onComplete {
	log.info ( workflow.success ? '\nDone!' : '\nOops .. something went wrong' )
}

