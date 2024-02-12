process analyze_dataset {
    publishDir "${params.output_dir}",
    mode:'copy'

    output:
    path "analysis/" , emit: analysis_outputs

    input:
    val config_file
    val experiment_name
    val data_path
    
    script:

    if (params.exp_name == "")
      """
      PYTHONPATH=$baseDir/bin/src analyze.py --analysis_config ${config_file} --experiment_dir ${experiment_name} --data_path ${data_path} 
      """

    else
      """
      PYTHONPATH=$baseDir/bin/src analyze.py --analysis_config ${config_file} --experiment_dir ${params.exp_name} --data_path ${data_path} 
      """

}
