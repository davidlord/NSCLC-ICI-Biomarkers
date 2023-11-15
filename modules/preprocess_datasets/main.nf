process fetch_dataset {
    publishDir params.outdir, mode: 'copy', saveAs: { file -> "${dataset_name}.${file}" }
    tag "${dataset_name}"

    input:
    path('data.csv')

    output:
    tuple val(dataset_name), path('data.txt'), path('meta.json'), emit: datasets

    script:
    """
    preprocessor.py -c preprocess_config.yml 
    """
}
