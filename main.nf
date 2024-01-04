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

log.info """\
        NSCLC-ICI pipeline
        ===============
        fetch_dataset   : ${params.fetch_dataset}
        dataset_names    : ${params.dataset_names}
        datatype    : ${params.datatype}

        visualize       : ${params.visualize}

        train           : ${params.train}
        mutations_data  : ${params.mutations_data}
        train_models    : ${params.train_models}

        predict         : ${params.predict}
        predict_models  : ${params.predict_models}
        predict_data    : ${params.predict_data}
        predict_meta    : ${params.predict_meta}

        output_dir        : ${params.output_dir}
        """
        .stripIndent()

/* 
 * main script flow
 */

workflow {
    mut_file       = Channel.fromPath("${params.mutations_data}")
    
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
    // otherwise load input files
    else {
        get_inputs()
        ch_premade_config = get_inputs.out.train_data.collect()
    }
}


process get_inputs {
    publishDir "${params.output_dir}"

    script:
        """
        echo GetInputs
        """
}

/* 
 * completion handler
 */
workflow.onComplete {
	log.info ( workflow.success ? '\nDone!' : '\nOops .. something went wrong' )
}
