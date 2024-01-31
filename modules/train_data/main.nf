process train_data {
    publishDir "${params.output_dir}",
    mode:'copy',
    saveAs: { fn ->
        fn ? "Modelling/${fn}" :
        fn
    }

    output:
    path "output/models/*/model/model.json", emit: model_json
    path "output/models/*/config/model_config.yml" , emit: config_copy

    input:
    path config

    script:
    """
    PYTHONPATH=$baseDir/bin/src train.py --config_path  $config 
    """
}
