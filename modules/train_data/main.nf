process train_data {
    publishDir "${params.output_dir}",
    mode:'copy',
    saveAs: { fn ->
        fn.endsWith('.tsv') ? "Modelling/output/models${fn}" :
        fn.endsWith('.yml') ? "configs/models/${fn}" :
        fn
    }

    output:
    path "*.yml" , emit: config_model
    path "test_data.csv" , emit: train_data
    path "train_data.csv", emit: infer_data

    input:
    path config

    script:
    """
    PYTHONPATH=$baseDir/bin/src train.py -c  $config --outdir ${params.output_dir} --outdir ${params.output_dir}
    """
}
