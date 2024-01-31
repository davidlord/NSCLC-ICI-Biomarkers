process infer_from_data {
    publishDir "${params.output_dir}",
    mode:'copy',
    saveAs: { fn ->
        fn.endsWith('.csv') ? "Modelling/${fn}" :
        fn.endsWith('.yml') ? "configs/analysis/${fn}" :
        fn
    }

    output:
    path "*.yml" , emit: config_preproc
    path "Modelling/output/models/*/inference/*.csv" , emit: infer_csv

    input:
    path experiment_name
    val infer_outfile 
    path data_path
    path config_file


    script:
    """
    PYTHONPATH=$baseDir/bin/src infer.py -c ${config_file} --experiment_folder ${experiment_name} --data_path ${data_path} --output_file ${infer_outfile} 
    """
}
