#!/usr/bin/env nextflow 

/*
 * Copyright (c) 2023, Clinical Genomics.
 * Distributed under the terms of the MIT License.
 */
import groovy.json.JsonSlurper

include { fetch_dataset } from './modules/fetch_dataset'
include { preprocess_datasets } from './modules/preprocess_datasets'
include { train_data} from './modules/train_data'
include { infer_from_data } from './modules/infer_from_data'
include { analyze_dataset } from './modules/analyze_dataset'

log.info """\
        PSM-DS pipeline
        ===============
        fetch_dataset   : ${params.fetch_dataset}
        dataset_name    : ${params.dataset_name}

        visualize       : ${params.visualize}

        train           : ${params.train}
        train_data      : ${params.train_data}
        train_meta      : ${params.train_meta}
        train_models    : ${params.train_models}

        predict         : ${params.predict}
        predict_models  : ${params.predict_models}
        predict_data    : ${params.predict_data}
        predict_meta    : ${params.predict_meta}

        outdir          : ${params.outdir}
        """
        .stripIndent()

/* 
 * main script flow
 */
workflow {
    // fetch dataset if specified
    if ( params.fetch_dataset == false ) {
        ch_datasets = fetch_dataset(params.datasets)

        (ch_train_datasets, ch_predict_datasets) = split_train_test(ch_datasets)
    }

    // otherwise load input files
    else {
        make_inputs()
        input_data = make_inputs.out.train_data.collect()
        train_data     = Channel.fromPath("${params.input_dir}/${params.train_data}").collect()
        mut_file       = Channel.fromPath("${params.input_dir}/${params.mut_file}")

    }

    // extract gene names from mutations file
    gene_sets = mut_file.flatMap {
        it.readLines().collect { line -> line.tokenize("\t")[0] }
    }

    mut_file = mut_file.collect()

     // visualize data sets
    if ( params.visualize == true ) {
        visualize(ch_datasets)
    }

    // print warning if both training and pre-trained model are enabled
    if ( params.train == true && params.predict_models != null ) {
        log.warn 'Training is enabled but pre-trained model(s) are also provided, pre-trained models will be ignored'
    }

    // perform training if specified
    if ( params.train == true ) {
        (ch_models, ch_train_logs) = train(ch_train_datasets, params.train_models)
    }

    // otherwise load trained model if specified
    else if ( params.predict_models != null ) {
        ch_models = Channel.fromFilePairs(params.predict_models, size: 1, flat: true)
            | map { [it[0], 'pretrained', it[1]] }
    }


 // perform inference if specified
    if ( params.predict == true ) {
        ch_predict_inputs = ch_models.combine(ch_predict_datasets, by: 0)
        (ch_scores, ch_predict_logs) = predict(ch_predict_inputs)

        // select the best model based on inference score
        ch_scores
            | max {
                new JsonSlurper().parse(it[2])['value']
            }
            | subscribe { dataset_name, model_type, score_file ->
                def score = new JsonSlurper().parse(score_file)
                println "The best model for \'${dataset_name}\' was \'${model_type}\', with ${score.name} = ${String.format('%.3f', score.value)}"
            }
    }
}


/* 
 * completion handler
 */
workflow.onComplete {
	log.info ( workflow.success ? '\nDone!' : '\nOops .. something went wrong' )
}