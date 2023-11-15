process fetch_dataset {
    publishDir params.outdir, mode: 'copy', saveAs: { file -> "${dataset_name}.${file}" }
    tag "${dataset_name}"

    input:
    val(dataset_name)

    output:
    path('preproc_config.yml'),  path('inputdata.txt'), path('meta.json'), emit: datasets

    script:
    """
    fetch-dataset.py --name ${dataset_name}
    """
}